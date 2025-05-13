# crawler/html_scraper.py
# -------------------------------------------------------------
from __future__ import annotations
import signal
from typing import List

from playwright.sync_api import sync_playwright, TimeoutError

from config import (
    CMC_BASE_URL, HEADLESS_LAUNCH,
    EXTRACTED_FIELDS, OUTPUT_CSV_PATH, SCROLL_COUNT, SCROLL_AMOUNT, SCROLL_PAUSE
)
from .filters  import select_columns
from .gdpr     import dismiss_banner
from .parser   import parse_row
from .exporter import save_csv


class CoinMarketCapHTMLScraper:
    def __init__(self):
        self.results: List[List[str]] = []
        self._stop_requested = False
        signal.signal(signal.SIGINT, self._sigint_handler)

    # ─────────────────────────────────────────────────────────
    def _sigint_handler(self, *_):
        print("\n[CTRL-C] Stop requested — finishing current page then exiting.")
        self._stop_requested = True

    # ─────────────────────────────────────────────────────────
    @staticmethod
    def _auto_scroll(page):
        for _ in range(SCROLL_COUNT):
            dismiss_banner(page)
            page.mouse.wheel(0, SCROLL_AMOUNT)
            page.wait_for_timeout(int(SCROLL_PAUSE * 1000))

    # ─────────────────────────────────────────────────────────
    def _parse_page(self, page):
        rows = page.locator("tbody tr")
        print(f"[Info] Found {rows.count()} rows")
        dismiss_banner(page)

        for i in range(rows.count()):
            if self._stop_requested:
                break
            row = rows.nth(i)
            self.results.append(parse_row(row, i))

    # ─────────────────────────────────────────────────────────
    def scrape_all(self, pages: int, row_limit: int):
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=HEADLESS_LAUNCH)
            page    = browser.new_page()

            try:
                for i in range(1, pages + 1):
                    if self._stop_requested or len(self.results) >= row_limit:
                        break

                    url = CMC_BASE_URL if i == 1 else f"{CMC_BASE_URL}?page={i}"
                    print(f"[Info] Fetching page {i}/{pages}: {url}")
                    page.goto(url, wait_until="networkidle")
                    dismiss_banner(page)

                    if i == 1:
                        select_columns(page)

                    self._auto_scroll(page)
                    self._parse_page(page)

            except TimeoutError as e:
                print(f"[Warn] Playwright timeout: {e}")

            finally:
                browser.close()

        print(f"[Info] Collected {len(self.results)} rows (requested {row_limit})")
        return self.results[:row_limit]

    # ─────────────────────────────────────────────────────────
    @staticmethod
    def to_csv(rows, path=OUTPUT_CSV_PATH):
        if not rows:
            print("[Error] No data collected – CSV not written.")
            return
        save_csv(rows, path, EXTRACTED_FIELDS)
