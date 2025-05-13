# crawler/price_fetcher.py

import requests
from config import CURRENCY, VS_CURRENCY

class PriceFetcher:
    def __init__(self, url):
        self.url = url
        self.failures = 0

    def fetch(self):
        response = requests.get(self.url, timeout=5)
        response.raise_for_status()
        data = response.json()
        price = data[CURRENCY][VS_CURRENCY]
        timestamp = data[CURRENCY]["last_updated_at"]
        return price, timestamp
