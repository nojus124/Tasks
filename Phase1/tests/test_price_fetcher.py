# tests/test_price_fetcher.py

from crawler.price_fetcher import PriceFetcher

def test_fetch_price(monkeypatch):
    def mock_get(*args, **kwargs):
        class MockResponse:
            def raise_for_status(self): pass
            def json(self):
                return {
                    "bitcoin": {
                        "usd": 50000,
                        "last_updated_at": 1710000000
                    }
                }
        return MockResponse()

    import requests
    monkeypatch.setattr(requests, "get", mock_get)

    fetcher = PriceFetcher("fake_url")
    price, timestamp = fetcher.fetch()

    assert price == 50000
    assert timestamp == 1710000000
