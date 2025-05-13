
# CoinMarketCap Crypto Crawler

A two‑phase Python project that provides **real‑time Bitcoin monitoring** (Phase 1) and a **market scraper of the top‑100 coins** on CoinMarketCap (Phase 2).  
Both phases run independently and share a consistent CSV schema.

---

## Phase 1 – Price Pulse

| Requirement                                   | Status |
|-----------------------------------------------|:------:|
| Poll CoinGecko every 1 s                      | ✔ |
| Keep last 10 prices                           | ✔ |
| Compute SMA (10)                              | ✔ |
| Exponential back‑off (1 → 2 → 4 s)            | ✔ |
| Continue after 5 consecutive failures         | ✔ |
| Graceful Ctrl‑C                               | ✔ |
| PyTest coverage for core logic                | ✔ |

Sample output

```
[2025‑04‑17T12:34:56] BTC → USD: $70 123.45    SMA(10): $69 980.12
```

Unit tests live under `Phase1/tests/` and cover:

* SMA window calculation
* Price fetcher

Run tests with:

```bash
pytest Phase1
```

---

## Phase 2 – CoinMarketCap Watchlist

### 2.1 HTML scraper (~200 LOC)

* Playwright‑powered; auto scrolls and paginates.  
* Table is processed **25 rows per page** → **100 rows = 4 pages**.  
* Extracts Rank, Name, Symbol, Price (USD), 24 h % Change, Market Cap (USD).  
* Fail‑safes: GDPR banner dismissal, network timeouts, graceful Ctrl‑C.  
* Saves to CSV via an OOP exporter.

### 2.2 JSON scraper (~140 LOC)

* Calls `https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing`.  
* Also 25‑coin pages; infinite retry with back‑off; graceful Ctrl‑C.  
* **Much faster** (≈ 3‑4 req/s) and simpler than HTML parsing.  
* Writes to the exact same CSV schema.

| Metric                  | HTML | JSON |
|-------------------------|-----:|-----:|
| Core LOC                | ~200 | ~140 |
| 100‑row runtime         | 25 s | 2 s |

---

## Installation

```bash
git clone https://github.com/nojus124/Tasks.git
cd Tasks
pip install -r requirements.txt
playwright install            # required for HTML scraper
```

---

## Usage

```bash
# Phase 1 – live Bitcoin ticker
python Phase1/main.py

# Phase 2 – HTML scraper (4 pages × 25 rows)
python Phase2/main.py --mode html  --pages 4 --rows 100 --out data/cmc_coins.csv

# Phase 2 – JSON scraper (same output, faster)
python Phase2/main.py --mode json  --pages 4 --rows 100 --out data/cmc_coins.csv
```

The CLI stops early if `--rows` is reached before all `--pages` are scraped.

---