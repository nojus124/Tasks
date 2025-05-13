
# CoinMarketCap Crypto Crawler

A two‑phase Python project that provides **real‑time Bitcoin monitoring** (Phase 1) and a **market scraper of the top‑100 coins** on CoinMarketCap (Phase 2).  
Both phases can be run independently and share a consistent CSV schema.

---

## Phase 1 – Price Pulse

| Requirement            | Implemented |
|------------------------|-------------|
| Poll CoinGecko every 1 s | ✔ |
| Keep last 10 prices    | ✔ |
| Compute SMA(10)        | ✔ |
| Exponential back‑off (1 → 2 → 4 s) | ✔ |
| Continue after 5 consecutive failures | ✔ |
| Graceful Ctrl‑C        | ✔ |

Sample output

```
[2025‑04‑17T12:34:56] BTC → USD: $70 123.45    SMA(10): $69 980.12
```

---

## Phase 2 – CoinMarketCap Watchlist

### 2.1 HTML scraper (≈ 200 LOC)

* Built with Playwright; scrolls + paginates automatically.  
* The watch‑list table is processed **25 rows per page** → **100 rows = 4 pages**.  
* Extracted fields: Rank, Name, Symbol, Price (USD), 24 h % Change, Market Cap (USD)  
* Added fail‑safes: cookie‑banner dismissal, network‑timeout handling, graceful Ctrl‑C.  
* Results saved via an OOP exporter to **CSV**.

### 2.2 JSON scraper (≈ 140 LOC)

* Uses `https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing`  
* Requests are 25 coins per call – identical page size to HTML.  
* Infinite retry with exponential back‑off; finishes in‑flight request on Ctrl‑C.  
* **Much faster** (≈ 3–4 requests/s) and avoids DOM / scrolling issues.  
* Writes to the same CSV schema as the HTML scraper.

| Metric                     | HTML | JSON |
|----------------------------|-----:|-----:|
| Lines of code (core)       | ~200 | ~140 |
| 100‑row runtime (typical)  |  25 s | 2 s |

---

## Installation

```bash
git clone https://github.com/nojus124/Tasks.git
cd Tasks
pip install -r requirements.txt
playwright install # required for the HTML scraper
```


---

## Usage

```bash
# Phase 1 – live Bitcoin ticker
python Phase1/main.py

# Phase 2 – HTML scraper (4 pages × 25 rows)
python Phase2/main.py --mode html --pages 4 --rows 100 --out data/cmc_coins.csv

# Phase 2 – JSON scraper (same output, faster)
python Phase2/main.py --mode json --pages 4 --rows 100 --out data/cmc_coins.csv
```

The CLI will automatically stop early if `--rows` is reached before `--pages`.

---