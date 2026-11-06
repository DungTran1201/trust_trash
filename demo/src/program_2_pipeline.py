# program_2_pipeline.py
import io
import re
import json
import struct
import hashlib
import urllib.parse
from pathlib import Path
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, Any, List, Optional

import requests
from bs4 import BeautifulSoup

# Thư viện xử lý PDF & Ảnh chuyên sâu (có cơ chế fallback an toàn nếu chưa cài)
try:
    from pypdf import PdfReader
    HAS_PYPDF = True
except ImportError:
    HAS_PYPDF = False

try:
    from PIL import Image
    HAS_PILLOW = True
except ImportError:
    HAS_PILLOW = False

from shared_platform import (
    PipelineConfig,
    TokenBucketRateLimiter,
    BandwidthThrottler,
    DataWarehouseManager,
    logger
)


class DataLakeAndWarehousePipeline:
    def __init__(self, config: PipelineConfig):
        self.config = config
        self.config.initialize_directories()
        self.rate_limiter = TokenBucketRateLimiter(
            rate_per_sec=config.requests_per_second,
            capacity=config.burst_capacity
        )
        self.bandwidth_throttler = BandwidthThrottler(max_kbps=config.max_bandwidth_kbps)
        self.dwh = DataWarehouseManager(config.dwh_db_path)
        self.semaphore = __import__("threading").BoundedSemaphore(config.max_workers)

        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/128.0.0.0 Safari/537.36"
            )
        })

    @staticmethod
    def _sanitize_name(text: str) -> str:
        clean = re.sub(r"[^a-zA-Z0-9_-]", "_", text.strip().lower())
        return re.sub(r"_+", "_", clean).strip("_") or "default"

    @staticmethod
    def _resolve_file_extension(url: str, content_type: str, category: str) -> str:
        parsed_path = urllib.parse.urlparse(url).path.lower()
        for ext in (".pdf", ".jpg", ".jpeg", ".png", ".webp", ".gif", ".svg", ".csv", ".docx", ".xlsx", ".zip", ".json"):
            if parsed_path.endswith(ext):
                return ext
        if "pdf" in content_type or category == "pdf":
            return ".pdf"
        if "png" in content_type:
            return ".png"
        if "webp" in content_type:
            return ".webp"
        if "gif" in content_type:
            return ".gif"
        if "jpeg" in content_type or "jpg" in content_type or category == "image":
            return ".jpg"
        return ".bin"

    def harvest_webpage_to_datalake(self, url_entry: Dict[str, str]) -> Optional[Path]:
        """Tải nội dung trang HTML gốc vào Data Lake."""
        url = url_entry["url"]
        keyword = url_entry["keyword"]
        domain = url_entry.get("domain") or "unknown_domain"
        doc_id = hashlib.sha256(url.encode("utf-8")).hexdigest()[:20]

        date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        kw_part = self._sanitize_name(keyword)
        html_dir = self.config.datalake_dir / f"keyword={kw_part}" / f"ingest_date={date_str}" / "html"
        html_dir.mkdir(parents=True, exist_ok=True)
        lake_file_path = html_dir / f"{doc_id}.json"

        with self.semaphore:
            self.rate_limiter.acquire()
            try:
                resp = self.session.get(url, stream=True, timeout=self.config.request_timeout)
                if resp.status_code != 200:
                    resp.close()
                    return None

                raw_buffer = bytearray()
                for chunk in resp.iter_content(chunk_size=8192):
                    if not chunk:
                        break
                    self.bandwidth_throttler.consume(len(chunk))
                    raw_buffer.extend(chunk)
                    if len(raw_buffer) >= self.config.max_html_bytes:
                        break
                resp.close()

                raw_html = raw_buffer.decode("utf-8", errors="replace")
                lake_record = {
                    "doc_id": doc_id,
                    "keyword": keyword,
                    "url": url,
                    "domain": domain,
                    "http_status": resp.status_code,
                    "byte_size": len(raw_buffer),
                    "ingested_at": datetime.now(timezone.utc).isoformat(),
                    "raw_html": raw_html
                }
                lake_file_path.write_text(json.dumps(lake_record, ensure_ascii=False, indent=2), encoding="utf-8")
                logger.info(f"[DataLake HTML] Đã lưu: {lake_file_path.name} ({len(raw_buffer)} bytes)")
                return lake_file_path
            except Exception as exc:
                logger.error(f"[DataLake HTML] Lỗi tải {url}: {exc}")
                return None

    def harvest_binary_asset_to_datalake(self, asset_entry: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Tải trực tiếp tệp nhị phân (PDF, Ảnh, Tài liệu) từ đường dẫn được phép truy cập
        và lưu thành tệp vật lý (.pdf, .jpg, .png...) bên trong Data Lake.
        """
        url = asset_entry["url"]
        keyword = asset_entry["keyword"]
        category = asset_entry.get("resource_category", "document")
        source_page = asset_entry.get("source_page_url", "")
        context_text = asset_entry.get("context_text", "")

        asset_id = hashlib.sha256(url.encode("utf-8")).hexdigest()[:20]
        date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        kw_part = self._sanitize_name(keyword)

        sub_folder = "pdf" if category == "pdf" else ("images" if category == "image" else "docs")
        asset_dir = (
            self.config.datalake_dir
            / f"keyword={kw_part}"
            / f"ingest_date={date_str}"
            / "assets"
            / sub_folder
        )
        asset_dir.mkdir(parents=True, exist_ok=True)

        with self.semaphore:
            self.rate_limiter.acquire()
            try:
                resp = self.session.get(url, stream=True, timeout=self.config.request_timeout)
                if resp.status_code != 200:
                    resp.close()
                    return None

                content_type = resp.headers.get("Content-Type", asset_entry.get("content_type", "")).lower()
                ext = self._resolve_file_extension(url, content_type, category)

                # Đặt tên tệp rõ ràng kết hợp tên gốc và mã băm
                url_stem = Path(urllib.parse.unquote(urllib.parse.urlparse(url).path)).stem
                clean_stem = self._sanitize_name(url_stem)[:40] or category
                binary_file_path = asset_dir / f"{clean_stem}_{asset_id[:10]}{ext}"

                sha256_hasher = hashlib.sha256()
                binary_buffer = bytearray()

                for chunk in resp.iter_content(chunk_size=16384):
                    if not chunk:
                        break
                    self.bandwidth_throttler.consume(len(chunk))
                    binary_buffer.extend(chunk)
                    sha256_hasher.update(chunk)
                    if len(binary_buffer) >= self.config.max_asset_bytes:
                        logger.warning(f"Chạm ngưỡng dung lượng tối đa ({self.config.max_asset_bytes} bytes) cho tệp: {url}")
                        break
                resp.close()

                if len(binary_buffer) == 0:
                    return None
                if category == "image" and len(binary_buffer) < self.config.min_image_bytes:
                    return None

                # Lưu tệp nhị phân thực tế xuống ổ đĩa Data Lake
                binary_file_path.write_bytes(binary_buffer)
                logger.info(
                    f"[DataLake ASSET - {category.upper()}] Đã tải tệp vật lý: "
                    f"{binary_file_path.name} ({len(binary_buffer) / 1024:.1f} KB)"
                )

                return {
                    "asset_id": asset_id,
                    "keyword": keyword,
                    "asset_url": url,
                    "source_page_url": source_page,
                    "asset_type": category,
                    "mime_type": content_type.split(";")[0].strip() or f"application/{ext.lstrip('.')}",
                    "file_extension": ext,
                    "file_size_bytes": len(binary_buffer),
                    "sha256_checksum": sha256_hasher.hexdigest(),
                    "context_caption": context_text,
                    "datalake_binary_path": str(binary_file_path),
                    "raw_bytes": bytes(binary_buffer),
                    "ingested_at": datetime.now(timezone.utc).isoformat()
                }
            except Exception as exc:
                logger.error(f"[DataLake ASSET] Lỗi khi tải tệp {url}: {exc}")
                return None

    def preprocess_binary_asset(self, asset_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Tiền xử lý tệp PDF / Ảnh đã tải trong Data Lake:
        - Nếu là PDF: Bóc tách số trang, metadata và toàn bộ nội dung chữ trong PDF.
        - Nếu là Ảnh: Bóc tách độ phân giải (Width x Height), hệ màu, định dạng.
        """
        asset_type = asset_info["asset_type"]
        raw_bytes: bytes = asset_info.pop("raw_bytes", b"")
        metadata: Dict[str, Any] = {}
        extracted_text = ""

        if asset_type == "pdf":
            if HAS_PYPDF:
                try:
                    reader = PdfReader(io.BytesIO(raw_bytes))
                    num_pages = len(reader.pages)
                    pdf_meta = reader.metadata or {}
                    metadata = {
                        "page_count": num_pages,
                        "title": str(pdf_meta.get("/Title", "") or "")[:200],
                        "author": str(pdf_meta.get("/Author", "") or "")[:150],
                        "creator": str(pdf_meta.get("/Creator", "") or "")[:150]
                    }
                    # Trích xuất văn bản từ tối đa 15 trang đầu của tệp PDF
                    text_chunks = []
                    for p_idx in range(min(num_pages, 15)):
                        page_txt = reader.pages[p_idx].extract_text() or ""
                        if page_txt:
                            text_chunks.append(page_txt)
                    extracted_text = re.sub(r"\s+", " ", " ".join(text_chunks)).strip()[:15000]
                except Exception as exc:
                    metadata = {"parse_note": f"PDF binary saved; text extraction warning: {str(exc)[:100]}"}
            else:
                # Fallback đếm số trang trực tiếp từ cấu trúc byte PDF nếu chưa cài pypdf
                page_matches = re.findall(rb"/Type\s*/Page\b", raw_bytes)
                metadata = {"estimated_page_count": len(page_matches), "parser": "native_binary_regex"}

        elif asset_type == "image":
            if HAS_PILLOW:
                try:
                    with Image.open(io.BytesIO(raw_bytes)) as img:
                        metadata = {
                            "width": img.width,
                            "height": img.height,
                            "format": img.format,
                            "mode": img.mode,
                            "aspect_ratio": round(img.width / max(img.height, 1), 2)
                        }
                except Exception as exc:
                    metadata = {"parse_note": f"Image binary saved; header note: {str(exc)[:80]}"}
            else:
                # Fallback đọc kích thước PNG trực tiếp từ byte header
                if raw_bytes.startswith(b"\x89PNG\r\n\x1a\n") and len(raw_bytes) >= 24:
                    w, h = struct.unpack(">II", raw_bytes[16:24])
                    metadata = {"width": w, "height": h, "format": "PNG"}

        asset_info["metadata_json"] = json.dumps(metadata, ensure_ascii=False)
        asset_info["extracted_text"] = extracted_text or asset_info.get("context_caption", "")
        asset_info["warehouse_synced_at"] = datetime.now(timezone.utc).isoformat()
        return asset_info

    @staticmethod
    def preprocess_html_payload(lake_record: Dict[str, Any], lake_file_path: Path) -> Optional[Dict[str, Any]]:
        raw_html = lake_record.get("raw_html", "")
        if not raw_html:
            return None

        soup = BeautifulSoup(raw_html, "lxml")
        page_title = soup.title.get_text(strip=True) if soup.title else ""
        meta_desc = ""
        meta_tag = soup.find("meta", attrs={"name": re.compile(r"^description$", re.I)})
        if meta_tag and meta_tag.get("content"):
            meta_desc = meta_tag.get("content").strip()

        heading_count = len(soup.find_all(["h1", "h2", "h3"]))
        embedded_assets_count = len(soup.find_all(["img", "embed", "iframe", "object"]))

        for noise_tag in soup(["script", "style", "noscript", "iframe", "svg", "header", "footer", "nav", "aside"]):
            noise_tag.decompose()

        clean_text = re.sub(r"\s+", " ", soup.get_text(separator=" ")).strip()
        word_count = len(clean_text.split())
        if word_count < 15:
            return None

        return {
            "doc_id": lake_record["doc_id"],
            "keyword": lake_record["keyword"],
            "url": lake_record["url"],
            "domain": lake_record["domain"],
            "page_title": page_title[:500],
            "meta_description": meta_desc[:1000],
            "clean_content": clean_text,
            "word_count": word_count,
            "heading_count": heading_count,
            "embedded_assets_found": embedded_assets_count,
            "datalake_file_path": str(lake_file_path),
            "ingested_at": lake_record["ingested_at"],
            "warehouse_synced_at": datetime.now(timezone.utc).isoformat()
        }

    def sync_all_to_datawarehouse(
        self,
        web_records: List[Dict[str, Any]],
        asset_records: List[Dict[str, Any]]
    ) -> Dict[str, int]:
        synced_pages = 0
        synced_assets = 0

        with self.dwh.db_lock:
            conn = self.dwh.get_connection()
            try:
                for rec in web_records:
                    row = conn.execute(
                        "SELECT keyword_id FROM dim_keywords WHERE keyword_text = ?",
                        (rec["keyword"],)
                    ).fetchone()
                    if not row:
                        continue

                    conn.execute(
                        """
                        INSERT INTO fact_web_documents (
                            doc_id, keyword_id, url, domain, page_title, meta_description,
                            clean_content, word_count, heading_count, embedded_assets_found,
                            datalake_file_path, ingested_at, warehouse_synced_at
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ON CONFLICT(doc_id) DO UPDATE SET
                            page_title = excluded.page_title,
                            clean_content = excluded.clean_content,
                            word_count = excluded.word_count,
                            embedded_assets_found = excluded.embedded_assets_found,
                            warehouse_synced_at = excluded.warehouse_synced_at
                        """,
                        (
                            rec["doc_id"], row["keyword_id"], rec["url"], rec["domain"],
                            rec["page_title"], rec["meta_description"], rec["clean_content"],
                            rec["word_count"], rec["heading_count"], rec["embedded_assets_found"],
                            rec["datalake_file_path"], rec["ingested_at"], rec["warehouse_synced_at"]
                        )
                    )
                    synced_pages += 1

                for asset in asset_records:
                    row = conn.execute(
                        "SELECT keyword_id FROM dim_keywords WHERE keyword_text = ?",
                        (asset["keyword"],)
                    ).fetchone()
                    if not row:
                        continue

                    conn.execute(
                        """
                        INSERT INTO fact_media_assets (
                            asset_id, keyword_id, asset_url, source_page_url, asset_type,
                            mime_type, file_extension, file_size_bytes, sha256_checksum,
                            context_caption, metadata_json, extracted_text,
                            datalake_binary_path, ingested_at, warehouse_synced_at
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ON CONFLICT(asset_id) DO UPDATE SET
                            file_size_bytes = excluded.file_size_bytes,
                            sha256_checksum = excluded.sha256_checksum,
                            metadata_json = excluded.metadata_json,
                            extracted_text = excluded.extracted_text,
                            datalake_binary_path = excluded.datalake_binary_path,
                            warehouse_synced_at = excluded.warehouse_synced_at
                        """,
                        (
                            asset["asset_id"], row["keyword_id"], asset["asset_url"],
                            asset["source_page_url"], asset["asset_type"], asset["mime_type"],
                            asset["file_extension"], asset["file_size_bytes"], asset["sha256_checksum"],
                            asset["context_caption"], asset["metadata_json"], asset["extracted_text"],
                            asset["datalake_binary_path"], asset["ingested_at"], asset["warehouse_synced_at"]
                        )
                    )
                    synced_assets += 1

                conn.commit()
            finally:
                conn.close()

        return {"pages": synced_pages, "assets": synced_assets}

    def run_etl_from_cache(self) -> None:
        if not self.config.cache_file.exists():
            logger.error("Không tìm thấy tệp Cache! Hãy chạy Chương trình 1 trước.")
            return

        cache_data = json.loads(self.config.cache_file.read_text(encoding="utf-8"))
        accepted_urls = cache_data.get("accepted_urls", [])
        accepted_assets = cache_data.get("accepted_assets", [])

        logger.info(
            f"Bắt đầu Chương trình 2: Tải {len(accepted_urls)} Webpages & "
            f"{len(accepted_assets)} tệp PDF/Ảnh/Tài liệu vào Data Lake..."
        )

        # 1. Tải song song các trang HTML
        html_files: List[Path] = []
        if accepted_urls:
            with ThreadPoolExecutor(max_workers=self.config.max_workers, thread_name_prefix="HTMLHarvester") as ex:
                futures = [ex.submit(self.harvest_webpage_to_datalake, u) for u in accepted_urls]
                for fut in as_completed(futures):
                    res_path = fut.result()
                    if res_path:
                        html_files.append(res_path)

        # 2. Tải song song các tệp nhị phân (PDF, Ảnh, Tài liệu)
        raw_downloaded_assets: List[Dict[str, Any]] = []
        if accepted_assets:
            with ThreadPoolExecutor(max_workers=self.config.max_workers, thread_name_prefix="AssetDownloader") as ex:
                futures = [ex.submit(self.harvest_binary_asset_to_datalake, a) for a in accepted_assets]
                for fut in as_completed(futures):
                    asset_data = fut.result()
                    if asset_data:
                        raw_downloaded_assets.append(asset_data)

        # 3. Tiền xử lý HTML & trích xuất chữ/metadata từ PDF, Ảnh
        cleaned_pages: List[Dict[str, Any]] = []
        for p in html_files:
            try:
                rec = json.loads(p.read_text(encoding="utf-8"))
                cleaned = self.preprocess_html_payload(rec, p)
                if cleaned:
                    cleaned_pages.append(cleaned)
            except Exception as e:
                logger.error(f"Lỗi tiền xử lý HTML {p}: {e}")

        processed_assets: List[Dict[str, Any]] = []
        for raw_asset in raw_downloaded_assets:
            try:
                processed_assets.append(self.preprocess_binary_asset(raw_asset))
            except Exception as e:
                logger.error(f"Lỗi tiền xử lý Asset {raw_asset.get('asset_url')}: {e}")

        # 4. Đồng bộ toàn bộ vào Data Warehouse
        sync_stats = self.sync_all_to_datawarehouse(cleaned_pages, processed_assets)
        logger.info(
            f"[DataWarehouse] Đồng bộ hoàn tất: {sync_stats['pages']} Webpages & "
            f"{sync_stats['assets']} tệp PDF/Ảnh/Tài liệu vào Data Warehouse!"
        )