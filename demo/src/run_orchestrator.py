# run_orchestrator.py
import argparse
import sys
from shared_platform import PipelineConfig, DataWarehouseManager, logger
from program_1_discovery import DiscoveryAndValidationEngine
from program_2_pipeline import DataLakeAndWarehousePipeline


def parse_cli_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="run_orchestrator.py",
        description="Deep Data Platform Pipeline: Chromium Multi-Hop DOM -> PDF/Image Asset Harvester -> Data Lake -> DWH",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    # Nhóm tham số Tìm kiếm & Quét sâu PDF/Ảnh
    search_group = parser.add_argument_group("Search & Deep Asset Discovery")
    search_group.add_argument(
        "-k", "--keywords",
        nargs="+",
        default=["machine learning architecture"],
        help="Danh sách từ khóa cần tìm kiếm và tải tài liệu/ảnh"
    )
    search_group.add_argument(
        "-l", "--lang",
        type=str,
        default="en",
        help="Ngôn ngữ tìm kiếm (vi, en, ja)"
    )
    search_group.add_argument(
        "--site",
        type=str,
        default="",
        help="Giới hạn trong một domain cụ thể (ví dụ: arxiv.org, github.com)"
    )
    search_group.add_argument(
        "--assets",
        nargs="+",
        choices=["pdf", "image", "document"],
        default=["pdf", "image", "document"],
        help="Các loại tệp nhị phân cần quét sâu và tải về Data Lake"
    )
    search_group.add_argument(
        "--deep-visits",
        type=int,
        default=3,
        help="Số lượng trang đích mà Chromium sẽ truy cập sâu vào bên trong để quét thẻ <img>, <iframe pdf>, <a pdf>"
    )
    search_group.add_argument(
        "--max-links",
        type=int,
        default=20,
        help="Số lượng đường dẫn tối đa kiểm tra ở tầng 1"
    )
    search_group.add_argument(
        "--max-assets-per-page",
        type=int,
        default=15,
        help="Số lượng tệp PDF/Ảnh tối đa trích xuất trên mỗi trang đích"
    )

    # Nhóm điều khiển hiển thị Chromium
    browser_group = parser.add_argument_group("Chromium Visual Controls")
    browser_group.add_argument(
        "--browser",
        type=str,
        choices=["chromium", "firefox"],
        default="chromium",
        help="Trình duyệt tự động hóa"
    )
    browser_group.add_argument(
        "--headless",
        action="store_true",
        default=False,
        help="Chạy ẩn trình duyệt (Mặc định là False để HIỂN THỊ trực tiếp cửa sổ Chromium)"
    )
    browser_group.add_argument(
        "--scrolls",
        type=int,
        default=3,
        help="Số lần cuộn trang tự động để kích hoạt ảnh lazy-load"
    )
    browser_group.add_argument(
        "--visual-delay",
        type=float,
        default=1.5,
        help="Độ trễ (giây) giữa các bước trên Chromium để dễ quan sát"
    )

    # Nhóm giới hạn Băng thông, Luồng & Rate Limit
    perf_group = parser.add_argument_group("Throttling, Concurrency & Limits")
    perf_group.add_argument("-w", "--workers", type=int, default=4, help="Số luồng tải song song tối đa")
    perf_group.add_argument("--rps", type=float, default=2.0, help="Giới hạn số request/giây")
    perf_group.add_argument("--bandwidth", type=float, default=512.0, help="Giới hạn băng thông (KB/s)")
    perf_group.add_argument("--min-img-kb", type=int, default=8, help="Kích thước ảnh tối thiểu (KB) để bỏ qua icon rác")

    # Chế độ chạy
    parser.add_argument(
        "-m", "--mode",
        choices=["all", "p1", "p2", "stats"],
        default="all",
        help="Chế độ chạy: 'all' (Toàn trình), 'p1' (Discovery & Cache), 'p2' (Download & ETL), 'stats' (Báo cáo DWH)"
    )

    return parser.parse_args()


def print_warehouse_summary(dwh_path) -> None:
    dwh = DataWarehouseManager(dwh_path)
    conn = dwh.get_connection()
    try:
        print("\n" + "=" * 85)
        print("1. THỐNG KÊ KIỂM TRA 3 TRẠNG THÁI THEO LOẠI TÀI NGUYÊN (WEBPAGE / PDF / IMAGE / DOC)")
        print("=" * 85)
        rows = conn.execute(
            """
            SELECT keyword_text, resource_category, validation_state, COUNT(*) as total
            FROM stg_url_validation
            GROUP BY keyword_text, resource_category, validation_state
            ORDER BY keyword_text, resource_category, validation_state
            """
        ).fetchall()
        for r in rows:
            print(
                f" - Keyword: {r['keyword_text']:<25} | Loại: {r['resource_category']:<9} | "
                f"Trạng thái: {r['validation_state']:<13} | Số lượng: {r['total']}"
            )

        print("\n" + "=" * 85)
        print("2. DANH SÁCH TỆP PDF, HÌNH ẢNH & TÀI LIỆU ĐÃ TẢI VỀ DATA LAKE & ĐỒNG BỘ DWH")
        print("=" * 85)
        assets = conn.execute(
            """
            SELECT asset_type, file_extension, file_size_bytes, metadata_json, datalake_binary_path
            FROM fact_media_assets
            ORDER BY file_size_bytes DESC
            LIMIT 15
            """
        ).fetchall()
        if not assets:
            print("Chưa có tệp PDF/Ảnh nào được tải về.")
        for a in assets:
            size_kb = a["file_size_bytes"] / 1024.0
            print(
                f" - [{a['asset_type'].upper():<5}] ({a['file_extension']}) | {size_kb:>8.1f} KB | "
                f"Meta: {a['metadata_json'][:42]:<42} | File: {a['datalake_binary_path']}"
            )
        print("=" * 85 + "\n")
    finally:
        conn.close()


def main():
    args = parse_cli_arguments()

    config = PipelineConfig(
        browser_type=args.browser,
        headless=args.headless,
        scroll_Count=args.scrolls,
        deep_visit_limit=args.deep_visits,
        allowed_asset_types=args.assets,
        max_workers=args.workers,
        requests_per_second=args.rps,
        max_bandwidth_kbps=args.bandwidth,
        min_image_bytes=args.min_img_kb * 1024
    )

    search_params = {
        "lang": args.lang,
        "site_filter": args.site,
        "visual_delay": args.visual_delay,
        "max_links_to_check": args.max_links,
        "max_assets_per_page": args.max_assets_per_page
    }

    if args.mode in ("all", "p1"):
        discovery_engine = DiscoveryAndValidationEngine(config)
        discovery_engine.execute_discovery(keywords=args.keywords, search_params=search_params)

    if args.mode in ("all", "p2"):
        etl_pipeline = DataLakeAndWarehousePipeline(config)
        etl_pipeline.run_etl_from_cache()

    print_warehouse_summary(config.dwh_db_path)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.warning("Đã dừng chương trình theo yêu cầu người dùng.")
        sys.exit(130)