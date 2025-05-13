# crawler/json_scraper.py
# -------------------------------------------------------------
"""
CoinMarketCap JSON scraper — fault-tolerant:
• Infinite retry with exponential back-off
• Graceful Ctrl-C: completes current request, writes partial results
"""

from __future__ import annotations
import signal, time
from typing import List

import requests
from requests.exceptions import HTTPError, Timeout, ConnectionError

from config import (
    EXTRACTED_FIELDS,
    OUTPUT_CSV_PATH,
    CMC_API_URL,
    PER_PAGE,
    BACKOFF_BASE,
    MAX_BACKOFF,
)
from .exporter import save_csv

class CoinMarketCapJSONScraper:
    def __init__(self):
        self.results: List[List[str]] = []
        self.session = requests.Session()          # ← no UA header
        self._stop_requested = False
        signal.signal(signal.SIGINT, self._sigint_handler)

    # ─────────────────────────────────────────────────────────
    def _sigint_handler(self, *_):
        print("\n[CTRL-C] Stop requested — finishing current request then exiting.")
        self._stop_requested = True

    # ─────────────────────────────────────────────────────────
    def _fetch_page(self, start: int) -> list:
        """Retry indefinitely until success or Ctrl-C."""
        attempt = 0
        while not self._stop_requested:
            try:
                r = self.session.get(
                    CMC_API_URL,
                    params={
                        "start":   start,
                        "limit":   PER_PAGE,
                        "sortBy":  "rank",
                        "sortType": "desc",
                        "convert": "USD",
                        "cryptoType": "all",
                    },
                    timeout=10,
                )
                r.raise_for_status()
                return r.json()["data"]["cryptoCurrencyList"]

            except (ConnectionError, Timeout) as e:
                attempt += 1
                wait = min(BACKOFF_BASE ** attempt, MAX_BACKOFF)
                print(f"[Warn] Network error {e} — retry in {wait:.1f}s (attempt {attempt})")
                time.sleep(wait)

            except HTTPError as e:
                if 500 <= r.status_code < 600:          # retry on server errors
                    attempt += 1
                    wait = min(BACKOFF_BASE ** attempt, MAX_BACKOFF)
                    print(f"[Warn] Server {r.status_code} — retry in {wait:.1f}s (attempt {attempt})")
                    time.sleep(wait)
                else:
                    print(f"[Error] HTTP {r.status_code}: {e} — skipping page")
                    return []

            except Exception as e:
                print(f"[Fatal] Unexpected: {e}")
                return []

        return []     # stop requested

    # ─────────────────────────────────────────────────────────
    @staticmethod
    def _row_from_json(obj: dict) -> list[str] | None:
        try:
            rank   = str(obj["cmcRank"])
            name   = obj["name"]
            symbol = obj["symbol"]
            usd    = next(q for q in obj["quotes"] if q.get("name") == "USD")
            price  = f'{usd["price"]:.2f}'
            change = f'{usd["percentChange24h"]:.2f}'
            mcap   = f'{usd["marketCap"]:.0f}'
            return [rank, name, symbol, price, change, mcap]
        except Exception:
            print(f"[Warn] Skipping malformed row id={obj.get('id')}")
            return None

    # ─────────────────────────────────────────────────────────
    def scrape_all(self, pages: int = 4, row_limit: int = 100) -> list[list[str]]:
        for idx in range(pages):
            if self._stop_requested or len(self.results) >= row_limit:
                break

            start = idx * PER_PAGE + 1
            print(f"[Info] Request page {idx+1}/{pages} (start={start})")

            rows = self._fetch_page(start)
            if self._stop_requested:
                break

            for obj in rows:
                if len(self.results) >= row_limit:
                    break
                row = self._row_from_json(obj)
                if row:
                    self.results.append(row)

        print(f"[Info] Collected {len(self.results)} rows (requested {row_limit})")
        return self.results[:row_limit]

    # ─────────────────────────────────────────────────────────
    @staticmethod
    def to_csv(rows: list[list[str]], path: str = OUTPUT_CSV_PATH):
        save_csv(rows, path, EXTRACTED_FIELDS)
