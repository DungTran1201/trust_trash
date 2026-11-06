# program_1_discovery.py
import re
import json
import time
import urllib.parse
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any, Optional, Set

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from shared_platform import (
    PipelineConfig,
    TokenBucketRateLimiter,
    BandwidthThrottler,
    DataWarehouseManager,
    logger
)

STATE_NULL = "null"
STATE_ACCEPTED = "accepted"
STATE_NOT_ACCEPTED = "not_accepted"

PDF_EXTENSIONS = (".pdf",)
IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp", ".gif", ".bmp", ".svg")
DOC_EXTENSIONS = (".csv", ".json", ".xml", ".docx", ".xlsx", ".pptx", ".zip", ".tar.gz")


class DiscoveryAndValidationEngine:
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
        adapter = requests.adapters.HTTPAdapter(
            pool_connections=config.max_workers,
            pool_maxsize=config.max_workers * 2,
            max_retries=1
        )
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        self.session.headers.update({
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/128.0.0.0 Safari/537.36"
            ),
            "Accept": "text/html,application/xhtml+xml,application/pdf,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7"
        })

    def _create_webdriver(self):
        if self.config.browser_type.lower() == "firefox":
            options = FirefoxOptions()
            if self.config.headless:
                options.add_argument("--headless")
            driver = webdriver.Firefox(options=options)
        else:
            options = ChromeOptions()
            if self.config.headless:
                options.add_argument("--headless=new")
            else:
                options.add_argument("--start-maximized")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            driver = webdriver.Chrome(options=options)

        driver.set_page_load_timeout(self.config.page_load_timeout)
        return driver

    @staticmethod
    def _update_browser_hud(driver, keyword: str, stage: str, status_text: str) -> None:
        """Hiển thị bảng HUD theo dõi trực tiếp các bước quét sâu trên góc phải màn hình Chromium."""
        js_hud = """
        (function(kw, stg, msg) {
            try {
                let hud = document.getElementById('__data_pipeline_hud__');
                if (!hud) {
                    hud = document.createElement('div');
                    hud.id = '__data_pipeline_hud__';
                    hud.style.cssText = [
                        'position: fixed', 'top: 16px', 'right: 16px', 'z-index: 2147483647',
                        'background: rgba(15, 23, 42, 0.94)', 'color: #38bdf8',
                        'font-family: Consolas, monospace', 'font-size: 13px',
                        'padding: 14px 18px', 'border-radius: 10px', 'border: 2px solid #0284c7',
                        'box-shadow: 0 10px 28px rgba(0,0,0,0.55)', 'max-width: 460px',
                        'pointer-events: none', 'line-height: 1.55'
                    ].join(';');
                    document.body.appendChild(hud);
                }
                hud.innerHTML = (
                    '<div style="color:#f8fafc;font-weight:bold;border-bottom:1px solid #334155;padding-bottom:5px;margin-bottom:6px;">' +
                    '⚡ DEEP ASSET & DOM SCANNER</div>' +
                    '<div><b>Keyword:</b> <span style="color:#fde047;">' + kw + '</span></div>' +
                    '<div><b>Stage:</b> <span style="color:#c084fc;">' + stg + '</span></div>' +
                    '<div><b>Action:</b> <span style="color:#4ade80;">' + msg + '</span></div>' +
                    '<div style="margin-top:6px;font-size:11px;color:#cbd5e1;">' +
                    '🟥 PDF/Docs &nbsp;|&nbsp; 🟧 Images &nbsp;|&nbsp; 🟩 Web Links</div>'
                );
            } catch (e) {}
        })(arguments[0], arguments[1], arguments[2]);
        """
        try:
            driver.execute_script(js_hud, keyword, stage, status_text)
        except Exception:
            pass

    @staticmethod
    def _highlight_deep_elements(driver) -> Dict[str, int]:
        """
        Đánh dấu màu trực tiếp trên giao diện Chromium:
        - Khung ĐỎ HỒNG (#f43f5e) cho các link/embed chứa tệp PDF hoặc tài liệu.
        - Khung CAM (#f59e0b) cho các thẻ Hình ảnh (<img>).
        - Khung XANH LÁ (#22c55e) cho các thẻ liên kết trang web (<a>).
        """
        js_highlight = """
        try {
            let counts = {pdf_docs: 0, images: 0, links: 0};
            document.querySelectorAll('a, iframe, embed, object').forEach(el => {
                const rawUrl = (el.getAttribute('href') || el.getAttribute('src') || el.getAttribute('data') || '').toLowerCase();
                if (rawUrl.match(/\\.(pdf|csv|docx|xlsx|pptx|zip)(\\?|$)/i) || rawUrl.includes('/pdf')) {
                    el.style.outline = '3px solid #f43f5e';
                    el.style.backgroundColor = 'rgba(244, 63, 94, 0.18)';
                    counts.pdf_docs += 1;
                } else if (el.tagName.toLowerCase() === 'a') {
                    el.style.outline = '1px dashed #22c55e';
                    counts.links += 1;
                }
            });
            document.querySelectorAll('img').forEach(img => {
                if ((img.naturalWidth || img.width || 0) >= 80) {
                    img.style.outline = '3px solid #f59e0b';
                    counts.images += 1;
                }
            });
            return counts;
        } catch (e) {
            return {pdf_docs: 0, images: 0, links: 0};
        }
        """
        try:
            res = driver.execute_script(js_highlight)
            return res if isinstance(res, dict) else {"pdf_docs": 0, "images": 0, "links": 0}
        except Exception:
            return {"pdf_docs": 0, "images": 0, "links": 0}

    @staticmethod
    def _extract_real_url(href: Any, base_url: str = "") -> Optional[str]:
        if not href or not isinstance(href, str):
            return None
        href = href.strip()
        if href.startswith(("javascript:", "mailto:", "tel:", "data:", "blob:", "#")):
            return href
        if "duckduckgo.com/l/?" in href or "uddg=" in href:
            parsed = urllib.parse.urlparse(href)
            qs = urllib.parse.parse_qs(parsed.query)
            if "uddg" in qs and qs["uddg"]:
                return urllib.parse.unquote(qs["uddg"][0])
        if base_url:
            return urllib.parse.urljoin(base_url, href)
        return href

    @staticmethod
    def _guess_category_from_url(url: str) -> str:
        if not url:
            return "webpage"
        parsed_path = urllib.parse.urlparse(url.lower()).path
        if parsed_path.endswith(PDF_EXTENSIONS) or "/pdf/" in parsed_path:
            return "pdf"
        if parsed_path.endswith(IMAGE_EXTENSIONS):
            return "image"
        if parsed_path.endswith(DOC_EXTENSIONS):
            return "document"
        return "webpage"

    def extract_assets_from_html(
        self,
        html_content: str,
        base_url: str,
        collect_images: bool = True
    ) -> List[Dict[str, str]]:
        """
        Quét sâu cây HTML bằng BeautifulSoup để lấy:
        1. Liên kết trang web & liên kết tải tệp trực tiếp (<a href>)
        2. Tệp PDF/Tài liệu nhúng (<iframe src>, <embed src>, <object data>)
        3. Hình ảnh (<img src/data-src/srcset>, <picture><source>) kèm chú thích ngữ cảnh
        """
        soup = BeautifulSoup(html_content, "lxml")
        discovered: List[Dict[str, str]] = []
        seen: Set[str] = set()

        # 1. Quét toàn bộ thẻ <a>
        for a_tag in soup.find_all("a"):
            raw_href = a_tag.get("href")
            resolved_url = self._extract_real_url(raw_href, base_url)
            anchor_text = a_tag.get_text(" ", strip=True)
            title_attr = a_tag.get("title", "")
            parent_text = a_tag.parent.get_text(" ", strip=True)[:200] if a_tag.parent else ""
            context = f"{anchor_text} {title_attr} {parent_text}".strip()

            key = f"{resolved_url}_{anchor_text[:15]}"
            if key in seen:
                continue
            seen.add(key)

            category = self._guess_category_from_url(resolved_url or "")
            discovered.append({
                "raw_href": resolved_url,
                "source_page_url": base_url,
                "expected_category": category,
                "context_text": context[:300]
            })

        # 2. Quét các khung nhúng PDF / Tài liệu (<iframe>, <embed>, <object>)
        for tag in soup.find_all(["iframe", "embed", "object"]):
            raw_src = tag.get("src") or tag.get("data")
            if not raw_src:
                continue
            resolved_url = self._extract_real_url(raw_src, base_url)
            if not resolved_url or resolved_url in seen:
                continue
            seen.add(resolved_url)

            cat = self._guess_category_from_url(resolved_url)
            if cat in ("pdf", "document") or "pdf" in resolved_url.lower():
                parent_ctx = tag.parent.get_text(" ", strip=True)[:250] if tag.parent else "Embedded Document"
                discovered.append({
                    "raw_href": resolved_url,
                    "source_page_url": base_url,
                    "expected_category": "pdf" if "pdf" in resolved_url.lower() else cat,
                    "context_text": parent_ctx
                })

        # 3. Quét toàn bộ thẻ Hình ảnh (<img>) nếu được bật
        if collect_images and "image" in self.config.allowed_asset_types:
            for img in soup.find_all("img"):
                # Xử lý cả ảnh lazy-load
                raw_src = (
                    img.get("src")
                    or img.get("data-src")
                    or img.get("data-lazy-src")
                    or img.get("data-original")
                )
                if not raw_src and img.get("srcset"):
                    first_srcset = img.get("srcset").split(",")[0].strip().split(" ")[0]
                    raw_src = first_srcset

                resolved_img = self._extract_real_url(raw_src, base_url)
                if not resolved_img or resolved_img.startswith("data:") or resolved_img in seen:
                    continue
                seen.add(resolved_img)

                # Bỏ qua các ảnh hiển nhiên là icon/logo/avatar/pixel nhỏ qua thuộc tính HTML
                width_attr = str(img.get("width", "")).replace("px", "").strip()
                height_attr = str(img.get("height", "")).replace("px", "").strip()
                if (width_attr.isdigit() and int(width_attr) < 64) or (height_attr.isdigit() and int(height_attr) < 64):
                    continue

                alt_text = img.get("alt", "").strip()
                title_text = img.get("title", "").strip()
                fig_caption = ""
                figure_parent = img.find_parent("figure")
                if figure_parent:
                    cap_tag = figure_parent.find("figcaption")
                    if cap_tag:
                        fig_caption = cap_tag.get_text(" ", strip=True)

                surrounding_text = img.parent.get_text(" ", strip=True)[:200] if img.parent else ""
                img_context = f"{alt_text} {title_text} {fig_caption} {surrounding_text}".strip()

                discovered.append({
                    "raw_href": resolved_img,
                    "source_page_url": base_url,
                    "expected_category": "image",
                    "context_text": img_context[:300]
                })

        return discovered

    def validate_single_candidate(self, keyword: str, candidate: Dict[str, str]) -> Dict[str, Any]:
        """
        Kiểm tra từng đường dẫn (Webpage, PDF, Image, Document) theo 3 trạng thái:
        - 'null': Đường dẫn rỗng, javascript/#, thiếu giao thức, hoặc phản hồi 0 byte / HTTP 204.
        - 'accepted': Tải được header/sample hợp lệ, đúng chữ ký tệp (Magic Bytes), đúng kích thước & liên quan từ khóa.
        - 'not_accepted': HTTP lỗi, sai định dạng, ảnh icon quá nhỏ, hoặc không liên quan từ khóa.
        """
        raw_url = candidate.get("raw_href")
        source_page = candidate.get("source_page_url", "")
        expected_cat = candidate.get("expected_category", "webpage")
        context_text = candidate.get("context_text", "")
        now_iso = datetime.now(timezone.utc).isoformat()

        # 1. Trạng thái NULL ở tầng cú pháp
        if not raw_url or raw_url.startswith(("#", "javascript:", "mailto:", "tel:", "data:", "blob:")):
            return {
                "keyword_text": keyword,
                "url": str(raw_url),
                "source_page_url": source_page,
                "resource_category": expected_cat,
                "domain": None,
                "context_text": context_text,
                "validation_state": STATE_NULL,
                "http_status": None,
                "content_type": None,
                "estimated_bytes": 0,
                "error_reason": "Null or non-downloadable URI scheme",
                "checked_at": now_iso
            }

        parsed = urllib.parse.urlparse(raw_url)
        if parsed.scheme not in ("http", "https") or not parsed.netloc:
            return {
                "keyword_text": keyword,
                "url": raw_url,
                "source_page_url": source_page,
                "resource_category": expected_cat,
                "domain": None,
                "context_text": context_text,
                "validation_state": STATE_NULL,
                "http_status": None,
                "content_type": None,
                "estimated_bytes": 0,
                "error_reason": "Missing HTTP/HTTPS scheme or domain",
                "checked_at": now_iso
            }

        blocked_domains = ("duckduckgo.com", "bing.com", "microsoft.com", "go.microsoft.com", "doubleclick.net")
        if any(d in parsed.netloc.lower() for d in blocked_domains):
            return {
                "keyword_text": keyword,
                "url": raw_url,
                "source_page_url": source_page,
                "resource_category": expected_cat,
                "domain": parsed.netloc,
                "context_text": context_text,
                "validation_state": STATE_NOT_ACCEPTED,
                "http_status": None,
                "content_type": None,
                "estimated_bytes": 0,
                "error_reason": "Filtered internal search engine or ad tracker domain",
                "checked_at": now_iso
            }

        # 2. Kiểm tra qua HTTP Stream kết hợp Rate Limit & Bandwidth Throttler
        with self.semaphore:
            self.rate_limiter.acquire()
            try:
                resp = self.session.get(
                    raw_url,
                    stream=True,
                    timeout=self.config.request_timeout,
                    allow_redirects=True
                )
                http_status = resp.status_code
                content_type = resp.headers.get("Content-Type", "").lower()
                content_length_hdr = resp.headers.get("Content-Length")
                estimated_bytes = int(content_length_hdr) if (content_length_hdr and content_length_hdr.isdigit()) else 0

                if http_status == 204:
                    resp.close()
                    return {
                        "keyword_text": keyword, "url": raw_url, "source_page_url": source_page,
                        "resource_category": expected_cat, "domain": parsed.netloc, "context_text": context_text,
                        "validation_state": STATE_NULL, "http_status": http_status, "content_type": content_type,
                        "estimated_bytes": 0, "error_reason": "HTTP 204 No Content", "checked_at": now_iso
                    }

                if http_status != 200:
                    resp.close()
                    return {
                        "keyword_text": keyword, "url": raw_url, "source_page_url": source_page,
                        "resource_category": expected_cat, "domain": parsed.netloc, "context_text": context_text,
                        "validation_state": STATE_NOT_ACCEPTED, "http_status": http_status, "content_type": content_type,
                        "estimated_bytes": estimated_bytes, "error_reason": f"HTTP {http_status}", "checked_at": now_iso
                    }

                # Xác định loại tài nguyên thực tế dựa trên MIME Type trả về từ Server
                actual_category = expected_cat
                if "application/pdf" in content_type:
                    actual_category = "pdf"
                elif content_type.startswith("image/"):
                    actual_category = "image"
                elif any(m in content_type for m in ("csv", "msword", "officedocument", "zip", "json")):
                    actual_category = "document"
                elif "text/html" in content_type:
                    actual_category = "webpage"

                # Đọc sample đầu tiên (tối đa 32KB) để kiểm tra chữ ký nhị phân (Magic Bytes) và độ liên quan
                sample_buf = bytearray()
                for chunk in resp.iter_content(chunk_size=4096):
                    if not chunk:
                        break
                    self.bandwidth_throttler.consume(len(chunk))
                    sample_buf.extend(chunk)
                    if len(sample_buf) >= 32768:
                        break
                resp.close()

                if len(sample_buf) == 0:
                    return {
                        "keyword_text": keyword, "url": raw_url, "source_page_url": source_page,
                        "resource_category": actual_category, "domain": parsed.netloc, "context_text": context_text,
                        "validation_state": STATE_NULL, "http_status": http_status, "content_type": content_type,
                        "estimated_bytes": 0, "error_reason": "Zero-byte payload", "checked_at": now_iso
                    }

                kw_tokens = [t.lower() for t in re.split(r"\W+", keyword) if len(t) > 1]
                url_and_ctx = f"{ urllib.parse.unquote(raw_url) } {context_text}".lower()

                # --- XỬ LÝ RIÊNG CHO TỆP PDF ---
                if actual_category == "pdf" or sample_buf.startswith(b"%PDF-"):
                    actual_category = "pdf"
                    if "pdf" not in self.config.allowed_asset_types:
                        return {
                            "keyword_text": keyword, "url": raw_url, "source_page_url": source_page,
                            "resource_category": "pdf", "domain": parsed.netloc, "context_text": context_text,
                            "validation_state": STATE_NOT_ACCEPTED, "http_status": http_status,
                            "content_type": content_type, "estimated_bytes": estimated_bytes or len(sample_buf),
                            "error_reason": "PDF collection disabled in config", "checked_at": now_iso
                        }
                    if not sample_buf.startswith(b"%PDF-"):
                        return {
                            "keyword_text": keyword, "url": raw_url, "source_page_url": source_page,
                            "resource_category": "pdf", "domain": parsed.netloc, "context_text": context_text,
                            "validation_state": STATE_NOT_ACCEPTED, "http_status": http_status,
                            "content_type": content_type, "estimated_bytes": len(sample_buf),
                            "error_reason": "Invalid PDF magic header", "checked_at": now_iso
                        }
                    return {
                        "keyword_text": keyword, "url": raw_url, "source_page_url": source_page,
                        "resource_category": "pdf", "domain": parsed.netloc, "context_text": context_text,
                        "validation_state": STATE_ACCEPTED, "http_status": http_status,
                        "content_type": "application/pdf", "estimated_bytes": estimated_bytes or len(sample_buf),
                        "error_reason": None, "checked_at": now_iso
                    }

                # --- XỬ LÝ RIÊNG CHO HÌNH ẢNH (IMAGE) ---
                if actual_category == "image":
                    if "image" not in self.config.allowed_asset_types:
                        return {
                            "keyword_text": keyword, "url": raw_url, "source_page_url": source_page,
                            "resource_category": "image", "domain": parsed.netloc, "context_text": context_text,
                            "validation_state": STATE_NOT_ACCEPTED, "http_status": http_status,
                            "content_type": content_type, "estimated_bytes": estimated_bytes,
                            "error_reason": "Image collection disabled", "checked_at": now_iso
                        }
                    # Loại bỏ ảnh quá nhỏ (icon, sprite, tracking pixel)
                    actual_size = estimated_bytes if estimated_bytes > 0 else len(sample_buf)
                    if actual_size < self.config.min_image_bytes:
                        return {
                            "keyword_text": keyword, "url": raw_url, "source_page_url": source_page,
                            "resource_category": "image", "domain": parsed.netloc, "context_text": context_text,
                            "validation_state": STATE_NOT_ACCEPTED, "http_status": http_status,
                            "content_type": content_type, "estimated_bytes": actual_size,
                            "error_reason": f"Image smaller than minimum threshold ({actual_size} bytes)",
                            "checked_at": now_iso
                        }
                    # Kiểm tra độ liên quan của ảnh qua alt/caption/URL hoặc trang nguồn đã được xác thực
                    is_img_relevant = any(t in url_and_ctx for t in kw_tokens) or bool(source_page)
                    if not is_img_relevant:
                        return {
                            "keyword_text": keyword, "url": raw_url, "source_page_url": source_page,
                            "resource_category": "image", "domain": parsed.netloc, "context_text": context_text,
                            "validation_state": STATE_NOT_ACCEPTED, "http_status": http_status,
                            "content_type": content_type, "estimated_bytes": actual_size,
                            "error_reason": "Image context unrelated to keyword", "checked_at": now_iso
                        }
                    return {
                        "keyword_text": keyword, "url": raw_url, "source_page_url": source_page,
                        "resource_category": "image", "domain": parsed.netloc, "context_text": context_text,
                        "validation_state": STATE_ACCEPTED, "http_status": http_status,
                        "content_type": content_type, "estimated_bytes": actual_size,
                        "error_reason": None, "checked_at": now_iso
                    }

                # --- XỬ LÝ CHO TÀI LIỆU KHÁC (CSV, DOCX, ZIP...) ---
                if actual_category == "document":
                    return {
                        "keyword_text": keyword, "url": raw_url, "source_page_url": source_page,
                        "resource_category": "document", "domain": parsed.netloc, "context_text": context_text,
                        "validation_state": STATE_ACCEPTED, "http_status": http_status,
                        "content_type": content_type, "estimated_bytes": estimated_bytes or len(sample_buf),
                        "error_reason": None, "checked_at": now_iso
                    }

                # --- XỬ LÝ CHO TRANG WEB HTML ---
                if "text/html" in content_type:
                    html_preview = sample_buf.decode("utf-8", errors="ignore").lower()
                    is_relevant = any(t in html_preview or t in url_and_ctx for t in kw_tokens)
                    if not is_relevant:
                        return {
                            "keyword_text": keyword, "url": raw_url, "source_page_url": source_page,
                            "resource_category": "webpage", "domain": parsed.netloc, "context_text": context_text,
                            "validation_state": STATE_NOT_ACCEPTED, "http_status": http_status,
                            "content_type": content_type, "estimated_bytes": len(sample_buf),
                            "error_reason": "HTML content does not match keyword", "checked_at": now_iso
                        }
                    return {
                        "keyword_text": keyword, "url": raw_url, "source_page_url": source_page,
                        "resource_category": "webpage", "domain": parsed.netloc, "context_text": context_text,
                        "validation_state": STATE_ACCEPTED, "http_status": http_status,
                        "content_type": content_type, "estimated_bytes": estimated_bytes or len(sample_buf),
                        "error_reason": None, "checked_at": now_iso
                    }

                return {
                    "keyword_text": keyword, "url": raw_url, "source_page_url": source_page,
                    "resource_category": actual_category, "domain": parsed.netloc, "context_text": context_text,
                    "validation_state": STATE_NOT_ACCEPTED, "http_status": http_status,
                    "content_type": content_type, "estimated_bytes": estimated_bytes,
                    "error_reason": f"Unsupported Content-Type: {content_type}", "checked_at": now_iso
                }

            except Exception as exc:
                return {
                    "keyword_text": keyword, "url": raw_url, "source_page_url": source_page,
                    "resource_category": expected_cat, "domain": parsed.netloc, "context_text": context_text,
                    "validation_state": STATE_NOT_ACCEPTED, "http_status": None,
                    "content_type": None, "estimated_bytes": 0,
                    "error_reason": str(exc)[:180], "checked_at": now_iso
                }

    def execute_discovery(self, keywords: List[str], search_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Thực thi quy trình Discovery 2 tầng trên Chromium:
        - Tầng 1: Quét trang tìm kiếm (kèm truy vấn filetype:pdf) -> Lọc ra Webpage & PDF trực tiếp.
        - Tầng 2: Điều khiển Chromium truy cập sâu vào bên trong các Webpage đã Accepted ->
                  Cuộn trang, tô sáng và bóc tách toàn bộ PDF, Ảnh (<img>), Tài liệu nhúng bên trong!
        """
        cached_payload: Dict[str, Any] = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "parameters": search_params,
            "valid_keywords": {},
            "accepted_urls": [],     # Danh sách trang HTML
            "accepted_assets": []    # Danh sách tệp PDF, Ảnh, Tài liệu cần tải về
        }

        lang = search_params.get("lang", "vi")
        site_filter = search_params.get("site_filter", "")
        visual_delay = float(search_params.get("visual_delay", 1.5))
        max_links = int(search_params.get("max_links_to_check", 25))
        max_assets_per_page = int(search_params.get("max_assets_per_page", 15))

        driver = None
        try:
            driver = self._create_webdriver()

            for kw in keywords:
                site_clause = f"site:{site_filter}" if site_filter else ""
                # Kết hợp tìm kiếm trang web thông thường VÀ truy vấn chuyên biệt săn tệp PDF
                q_general = urllib.parse.quote_plus(f"{kw} {site_clause}".strip())
                q_pdf = urllib.parse.quote_plus(f"{kw} filetype:pdf {site_clause}".strip())

                seed_urls = [
                    ("Search Engine (Web & Media)", f"https://duckduckgo.com/?q={q_general}&kl={lang}-{lang}&ia=web"),
                ]
                if "pdf" in self.config.allowed_asset_types:
                    seed_urls.append(
                        ("Search Engine (Direct PDF Hunt)", f"https://duckduckgo.com/?q={q_pdf}&kl={lang}-{lang}&ia=web")
                    )

                hop1_candidates: List[Dict[str, str]] = []
                for stage_label, s_url in seed_urls:
                    self.rate_limiter.acquire()
                    logger.info(f"[Hop 1 - {stage_label}] Chromium đang truy cập: {s_url}")
                    driver.get(s_url)
                    WebDriverWait(driver, 12).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

                    self._update_browser_hud(driver, kw, stage_label, "Đang cuộn giao diện tìm kiếm...")
                    for _ in range(self.config.scroll_Count):
                        driver.execute_script("window.scrollBy({top: 650, left: 0, behavior: 'smooth'});")
                        time.sleep(visual_delay if not self.config.headless else 0.6)

                    counts = self._highlight_deep_elements(driver)
                    self._update_browser_hud(
                        driver, kw, stage_label,
                        f"Phát hiện {counts['links']} Web Links & {counts['pdf_docs']} PDF Links!"
                    )
                    if not self.config.headless:
                        time.sleep(visual_delay)

                    extracted = self.extract_assets_from_html(
                        driver.page_source, base_url=s_url, collect_images=False
                    )
                    hop1_candidates.extend(extracted)

                hop1_candidates = hop1_candidates[:max_links]
                logger.info(f"[Hop 1] Đang kiểm tra 3 trạng thái cho {len(hop1_candidates)} đường dẫn nguồn...")

                all_validation_records: List[Dict[str, Any]] = []
                accepted_webpages: List[Dict[str, Any]] = []
                accepted_assets: List[Dict[str, Any]] = []

                with ThreadPoolExecutor(max_workers=self.config.max_workers, thread_name_prefix="Hop1Validator") as ex:
                    futures = [ex.submit(self.validate_single_candidate, kw, c) for c in hop1_candidates]
                    for fut in as_completed(futures):
                        res = fut.result()
                        all_validation_records.append(res)
                        if res["validation_state"] == STATE_ACCEPTED:
                            if res["resource_category"] == "webpage":
                                accepted_webpages.append(res)
                            else:
                                accepted_assets.append(res)

                # --- TẦNG 2 (HOP 2): TRUY CẬP SÂU VÀO TRANG ĐÍCH ĐỂ SĂN PDF & ẢNH NHÚNG ---
                pages_to_deep_crawl = accepted_webpages[:self.config.deep_visit_limit]
                deep_asset_candidates: List[Dict[str, str]] = []

                for idx, page_info in enumerate(pages_to_deep_crawl, start=1):
                    target_url = page_info["url"]
                    stage_name = f"Hop 2 - Deep Target Crawl ({idx}/{len(pages_to_deep_crawl)})"
                    logger.info(f"[{stage_name}] Chromium đang tiến vào trang đích: {target_url}")

                    try:
                        self.rate_limiter.acquire()
                        driver.get(target_url)
                        WebDriverWait(driver, 12).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

                        self._update_browser_hud(
                            driver, kw, stage_name,
                            f"Đang cuộn trang đích để kích hoạt ảnh lazy-load & tài liệu PDF nhúng..."
                        )
                        for _ in range(self.config.scroll_Count):
                            driver.execute_script("window.scrollBy({top: 750, left: 0, behavior: 'smooth'});")
                            time.sleep(visual_delay if not self.config.headless else 0.6)

                        hl_stats = self._highlight_deep_elements(driver)
                        self._update_browser_hud(
                            driver, kw, stage_name,
                            f"Đã khoanh vùng: {hl_stats['pdf_docs']} PDF/Docs (Đỏ) | {hl_stats['images']} Ảnh (Cam)!"
                        )
                        if not self.config.headless:
                            time.sleep(visual_delay)

                        # Quét toàn bộ DOM của trang đích để lấy link PDF, <iframe>, <embed> và <img>
                        page_assets = self.extract_assets_from_html(
                            driver.page_source, base_url=target_url, collect_images=True
                        )
                        # Chỉ lọc lấy các phần tử là PDF, Image hoặc Document từ trang đích
                        media_only = [
                            a for a in page_assets
                            if a["expected_category"] in ("pdf", "image", "document")
                        ][:max_assets_per_page]
                        deep_asset_candidates.extend(media_only)

                    except Exception as e:
                        logger.warning(f"Không thể quét sâu trang đích {target_url}: {e}")

                if deep_asset_candidates:
                    logger.info(
                        f"[Hop 2] Đang kiểm tra 3 trạng thái cho {len(deep_asset_candidates)} "
                        f"tệp PDF/Ảnh/Tài liệu tìm thấy bên trong các trang đích..."
                    )
                    with ThreadPoolExecutor(max_workers=self.config.max_workers, thread_name_prefix="Hop2AssetVal") as ex:
                        futures = [ex.submit(self.validate_single_candidate, kw, c) for c in deep_asset_candidates]
                        for fut in as_completed(futures):
                            res = fut.result()
                            all_validation_records.append(res)
                            if res["validation_state"] == STATE_ACCEPTED and res["resource_category"] != "webpage":
                                accepted_assets.append(res)

                # Thống kê kết quả 3 trạng thái
                st_summary = {STATE_NULL: 0, STATE_ACCEPTED: 0, STATE_NOT_ACCEPTED: 0}
                for r in all_validation_records:
                    st_summary[r["validation_state"]] = st_summary.get(r["validation_state"], 0) + 1

                logger.info(
                    f"Tổng kết từ khóa '{kw}': ACCEPTED={st_summary[STATE_ACCEPTED]} "
                    f"(Webpages={len(accepted_webpages)}, PDF/Images/Docs={len(accepted_assets)}) | "
                    f"NOT_ACCEPTED={st_summary[STATE_NOT_ACCEPTED]} | NULL={st_summary[STATE_NULL]}"
                )

                # Lưu vào DB Staging & Dimension
                self._persist_validation_results(
                    kw, search_params, all_validation_records,
                    len(accepted_webpages), len(accepted_assets)
                )

                # Đưa vào Cache cho Chương trình 2 tải về Data Lake
                if accepted_webpages or accepted_assets:
                    cached_payload["valid_keywords"][kw] = {
                        "accepted_webpages": len(accepted_webpages),
                        "accepted_assets": len(accepted_assets),
                        "last_verified": datetime.now(timezone.utc).isoformat()
                    }
                    seen_page_urls = {u["url"] for u in cached_payload["accepted_urls"]}
                    for p in accepted_webpages:
                        if p["url"] not in seen_page_urls:
                            cached_payload["accepted_urls"].append({
                                "keyword": kw,
                                "url": p["url"],
                                "domain": p["domain"],
                                "context_text": p["context_text"],
                                "cached_at": p["checked_at"]
                            })
                            seen_page_urls.add(p["url"])

                    seen_asset_urls = {a["url"] for a in cached_payload["accepted_assets"]}
                    for asset in accepted_assets:
                        if asset["url"] not in seen_asset_urls:
                            cached_payload["accepted_assets"].append({
                                "keyword": kw,
                                "url": asset["url"],
                                "source_page_url": asset["source_page_url"],
                                "resource_category": asset["resource_category"],
                                "content_type": asset["content_type"],
                                "domain": asset["domain"],
                                "context_text": asset["context_text"],
                                "estimated_bytes": asset["estimated_bytes"],
                                "cached_at": asset["checked_at"]
                            })
                            seen_asset_urls.add(asset["url"])

        finally:
            if driver:
                driver.quit()

        self.config.cache_file.write_text(
            json.dumps(cached_payload, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
        logger.info(
            f"Đã ghi Cache: {len(cached_payload['accepted_urls'])} Webpages & "
            f"{len(cached_payload['accepted_assets'])} tệp PDF/Ảnh/Docs tại {self.config.cache_file}"
        )
        return cached_payload

    def _persist_validation_results(
        self,
        keyword: str,
        search_params: Dict[str, Any],
        results: List[Dict[str, Any]],
        accepted_pages_count: int,
        accepted_assets_count: int
    ) -> None:
        now_iso = datetime.now(timezone.utc).isoformat()
        with self.dwh.db_lock:
            conn = self.dwh.get_connection()
            try:
                for r in results:
                    conn.execute(
                        """
                        INSERT INTO stg_url_validation (
                            keyword_text, url, source_page_url, resource_category, domain,
                            context_text, validation_state, http_status, content_type,
                            estimated_bytes, error_reason, checked_at
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ON CONFLICT(keyword_text, url) DO UPDATE SET
                            validation_state = excluded.validation_state,
                            resource_category = excluded.resource_category,
                            http_status = excluded.http_status,
                            content_type = excluded.content_type,
                            estimated_bytes = excluded.estimated_bytes,
                            error_reason = excluded.error_reason,
                            checked_at = excluded.checked_at
                        """,
                        (
                            r["keyword_text"], r["url"], r["source_page_url"], r["resource_category"],
                            r["domain"], r["context_text"], r["validation_state"], r["http_status"],
                            r["content_type"], r["estimated_bytes"], r["error_reason"], r["checked_at"]
                        )
                    )

                if (accepted_pages_count + accepted_assets_count) > 0:
                    conn.execute(
                        """
                        INSERT INTO dim_keywords (
                            keyword_text, search_params, accepted_pages_count,
                            accepted_assets_count, discovered_at, updated_at
                        ) VALUES (?, ?, ?, ?, ?, ?)
                        ON CONFLICT(keyword_text) DO UPDATE SET
                            accepted_pages_count = excluded.accepted_pages_count,
                            accepted_assets_count = excluded.accepted_assets_count,
                            updated_at = excluded.updated_at
                        """,
                        (
                            keyword, json.dumps(search_params, ensure_ascii=False),
                            accepted_pages_count, accepted_assets_count, now_iso, now_iso
                        )
                    )
                conn.commit()
            finally:
                conn.close()