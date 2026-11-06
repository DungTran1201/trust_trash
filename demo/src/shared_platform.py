# shared_platform.py
import time
import sqlite3
import logging
import threading
from pathlib import Path
from dataclasses import dataclass, field
from typing import List

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | [%(levelname)s] | [%(threadName)s] | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("DataPlatform")


@dataclass
class PipelineConfig:
    # Tham số trình duyệt & Deep Crawl
    browser_type: str = "chromium"
    headless: bool = False                  # Mặc định mở UI Chromium để quan sát
    page_load_timeout: int = 25
    scroll_Count: int = 3
    deep_visit_limit: int = 3               # Số trang đích Chromium sẽ truy cập sâu để quét PDF/Ảnh nhúng
    allowed_asset_types: List[str] = field(default_factory=lambda: ["pdf", "image", "document"])

    # Tham số chống nghẽn cổ chai & giới hạn dung lượng tệp tải về
    max_workers: int = 4
    requests_per_second: float = 2.0
    burst_capacity: int = 4
    max_bandwidth_kbps: float = 512.0       # Giới hạn băng thông tổng (KB/s)
    max_html_bytes: int = 2 * 1024 * 1024   # Tối đa 2MB cho trang HTML
    max_asset_bytes: int = 20 * 1024 * 1024 # Tối đa 20MB cho tệp PDF / Ảnh chất lượng cao
    min_image_bytes: int = 8 * 1024         # Bỏ qua ảnh icon/tracking pixel nhỏ hơn 8KB
    request_timeout: int = 15

    # Đường dẫn lưu trữ Data Platform
    base_dir: Path = Path("./data_platform_storage")
    cache_file: Path = Path("./data_platform_storage/cache/accepted_urls_cache.json")
    datalake_dir: Path = Path("./data_platform_storage/datalake/bronze_raw")
    dwh_db_path: Path = Path("./data_platform_storage/datawarehouse/enterprise_dwh.db")

    def initialize_directories(self) -> None:
        self.cache_file.parent.mkdir(parents=True, exist_ok=True)
        self.datalake_dir.mkdir(parents=True, exist_ok=True)
        self.dwh_db_path.parent.mkdir(parents=True, exist_ok=True)


class TokenBucketRateLimiter:
    """Giới hạn tần suất gửi request (Rate Limiter) an toàn cho đa luồng."""
    def __init__(self, rate_per_sec: float, capacity: int):
        self.rate = float(rate_per_sec)
        self.capacity = float(capacity)
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()
        self.lock = threading.Lock()

    def acquire(self) -> None:
        while True:
            with self.lock:
                now = time.monotonic()
                elapsed = now - self.last_refill
                self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
                self.last_refill = now

                if self.tokens >= 1.0:
                    self.tokens -= 1.0
                    return
                wait_time = (1.0 - self.tokens) / self.rate
            time.sleep(wait_time)


class BandwidthThrottler:
    """Kiểm soát băng thông mạng (KB/s) khi tải stream HTML, PDF và Hình ảnh."""
    def __init__(self, max_kbps: float):
        self.max_bytes_per_sec = max_kbps * 1024.0
        self.bytes_transferred = 0
        self.window_start = time.monotonic()
        self.lock = threading.Lock()

    def consume(self, byte_count: int) -> None:
        if self.max_bytes_per_sec <= 0:
            return
        with self.lock:
            now = time.monotonic()
            elapsed = now - self.window_start
            if elapsed >= 1.0:
                self.window_start = now
                self.bytes_transferred = 0
                elapsed = 0.0

            self.bytes_transferred += byte_count
            expected_time = self.bytes_transferred / self.max_bytes_per_sec
            if expected_time > elapsed:
                time.sleep(expected_time - elapsed)


class DataWarehouseManager:
    """Quản lý Schema SQLite Data Warehouse hỗ trợ lưu trữ cả Webpage và Media/File Assets."""
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.db_lock = threading.Lock()
        self._init_schema()

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self.db_path), timeout=30.0, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_schema(self) -> None:
        schema_sql = """
        PRAGMA journal_mode = WAL;
        PRAGMA synchronous = NORMAL;
        PRAGMA foreign_keys = ON;

        -- Bảng Dimension lưu từ khóa có dữ liệu truy xuất thành công
        CREATE TABLE IF NOT EXISTS dim_keywords (
            keyword_id INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword_text TEXT NOT NULL UNIQUE,
            search_params TEXT NOT NULL,
            accepted_pages_count INTEGER DEFAULT 0,
            accepted_assets_count INTEGER DEFAULT 0,
            discovered_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

        -- Bảng Staging ghi nhận 3 trạng thái (null, accepted, not_accepted) cho mọi đường dẫn & tệp
        CREATE TABLE IF NOT EXISTS stg_url_validation (
            url_id INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword_text TEXT NOT NULL,
            url TEXT NOT NULL,
            source_page_url TEXT,
            resource_category TEXT NOT NULL, -- 'webpage', 'pdf', 'image', 'document'
            domain TEXT,
            context_text TEXT,
            validation_state TEXT NOT NULL CHECK(validation_state IN ('null', 'accepted', 'not_accepted')),
            http_status INTEGER,
            content_type TEXT,
            estimated_bytes INTEGER,
            error_reason TEXT,
            checked_at TEXT NOT NULL,
            UNIQUE(keyword_text, url)
        );

        -- Bảng Fact 1: Lưu trữ nội dung văn bản các trang web
        CREATE TABLE IF NOT EXISTS fact_web_documents (
            doc_id TEXT PRIMARY KEY,
            keyword_id INTEGER NOT NULL,
            url TEXT NOT NULL UNIQUE,
            domain TEXT NOT NULL,
            page_title TEXT,
            meta_description TEXT,
            clean_content TEXT NOT NULL,
            word_count INTEGER NOT NULL,
            heading_count INTEGER NOT NULL,
            embedded_assets_found INTEGER DEFAULT 0,
            datalake_file_path TEXT NOT NULL,
            ingested_at TEXT NOT NULL,
            warehouse_synced_at TEXT NOT NULL,
            FOREIGN KEY (keyword_id) REFERENCES dim_keywords(keyword_id)
        );

        -- Bảng Fact 2: Lưu trữ chuyên biệt các tệp PDF, Hình ảnh và Tài liệu tải về từ trang đích
        CREATE TABLE IF NOT EXISTS fact_media_assets (
            asset_id TEXT PRIMARY KEY,
            keyword_id INTEGER NOT NULL,
            asset_url TEXT NOT NULL UNIQUE,
            source_page_url TEXT,
            asset_type TEXT NOT NULL,          -- 'pdf', 'image', 'document'
            mime_type TEXT NOT NULL,
            file_extension TEXT NOT NULL,
            file_size_bytes INTEGER NOT NULL,
            sha256_checksum TEXT NOT NULL,
            context_caption TEXT,              -- Chú thích ảnh (alt/figcaption) hoặc tiêu đề link PDF
            metadata_json TEXT,                -- Độ phân giải ảnh (WxH) hoặc số trang/tác giả PDF
            extracted_text TEXT,               -- Nội dung chữ trích xuất từ PDF
            datalake_binary_path TEXT NOT NULL,-- Đường dẫn tệp vật lý (.pdf, .png, .jpg) trong Data Lake
            ingested_at TEXT NOT NULL,
            warehouse_synced_at TEXT NOT NULL,
            FOREIGN KEY (keyword_id) REFERENCES dim_keywords(keyword_id)
        );

        CREATE INDEX IF NOT EXISTS idx_stg_state ON stg_url_validation(validation_state, resource_category);
        CREATE INDEX IF NOT EXISTS idx_asset_type ON fact_media_assets(asset_type);
        """
        with self.db_lock:
            conn = self.get_connection()
            try:
                conn.executescript(schema_sql)
                conn.commit()
            finally:
                conn.close()