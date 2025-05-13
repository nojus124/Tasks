# crawler/scheduler.py

import time
import datetime
import traceback

from crawler.price_fetcher import PriceFetcher
from crawler.moving_average import MovingAverage
from config import LOG_FORMAT, DATE_FORMAT

class Scheduler:
    def __init__(self, url, poll_interval, sma_window, max_retries, initial_backoff):
        self.poll_interval = poll_interval
        self.max_retries = max_retries
        self.initial_backoff = initial_backoff
        self.running = True
        self.fetcher = PriceFetcher(url)
        self.sma = MovingAverage(sma_window)

    def run(self):
        while self.running:
            try:
                price, timestamp = self._try_fetch_price()
                avg = self.sma.update(price)
                formatted_time = datetime.datetime.utcfromtimestamp(timestamp).isoformat()
                print(f"[{formatted_time}] BTC → USD: ${price:,.2f}   SMA(10): ${avg:,.2f}")
                time.sleep(self.poll_interval)
            except Exception as e:
                print(f"Fatal error: {e}")
                traceback.print_exc()

    def _try_fetch_price(self):
        retries = 0
        backoff = self.initial_backoff
        while retries < self.max_retries:
            try:
                return self.fetcher.fetch()
            except Exception as e:
                retries += 1
                print(f"Fetch failed (attempt {retries}): {e}. Retrying in {backoff}s…")
                time.sleep(backoff)
                backoff *= 2
        print("Max retries reached. Continuing polling loop…")
        raise RuntimeError("Too many fetch failures.")

    def shutdown(self):
        self.running = False
