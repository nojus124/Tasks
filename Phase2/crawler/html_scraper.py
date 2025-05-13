from playwright.sync_api import sync_playwright
from config import (
    CMC_BASE_URL,
    CMC_PAGE_LIMIT,
    ROW_LIMIT,
    HEADLESS_LAUNCH,
    EXTRACTED_FIELDS,
    OUTPUT_CSV_PATH,
)
from .filters import select_columns
from .gdpr import dismiss_banner
from .parser import parse_row
from .exporter import save_csv


class CoinMarketCapHTMLScraper:
    def __init__(self):
        self.results = []
        self.column_map = {}

    def auto_scroll(self, page):
        from config import SCROLL_COUNT, SCROLL_AMOUNT, SCROLL_PAUSE
        for _ in range(SCROLL_COUNT):
            dismiss_banner(page)
            page.mouse.wheel(0, SCROLL_AMOUNT)
            page.wait_for_timeout(int(SCROLL_PAUSE * 1000))

    def parse_page(self, page):
        rows = page.locator("tbody tr")
        print(f"[Info] Found {rows.count()} rows")
        dismiss_banner(page)

        for i in range(rows.count()):
            row = rows.nth(i)
            self.results.append(parse_row(row, i))

    def scrape_all(self, pages=CMC_PAGE_LIMIT, row_limit=ROW_LIMIT):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=HEADLESS_LAUNCH)
            page = browser.new_page()

            for i in range(1, pages + 1):
                if len(self.results) >= row_limit:
                    break

                url = CMC_BASE_URL if i == 1 else f"{CMC_BASE_URL}?page={i}"
                print(f"[Info] Fetching page {i}: {url}")
                page.goto(url, wait_until="networkidle")
                dismiss_banner(page)

                if i == 1:
                    select_columns(page)

                self.auto_scroll(page)
                self.parse_page(page)

            browser.close()

        return self.results[:row_limit]

    def to_csv(self, rows, path=OUTPUT_CSV_PATH):
        save_csv(rows, path, EXTRACTED_FIELDS)
