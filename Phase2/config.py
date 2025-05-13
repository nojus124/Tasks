# config.py

# Output file path (CSV)
OUTPUT_CSV_PATH = "data/cmc_coins.csv"

# Fields to extract (for validation/testing if needed)
EXTRACTED_FIELDS = [
    "Rank",
    "Name",
    "Symbol",
    "Price (USD)",
    "24h % Change",
    "Market Cap (USD)"
]

# HTML Scraper settings
HEADLESS_LAUNCH = True
CMC_BASE_URL = "https://coinmarketcap.com/" # Base URL for HTML pages
SCROLL_COUNT = 12 # How many times to scroll down the page to trigger lazy loading
SCROLL_PAUSE = 0.6 # Delay (in seconds) between scrolls — increase if content loads slowly
SCROLL_AMOUNT = 1000 # Number of pixels to scroll per step — higher values scroll faster (with higher values cannot catch ajax)
# Try 500 for smoother gradual loading
# HTML Scraper settings end

# JSON API scraper settings
CMC_API_URL = "https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing"
PER_PAGE = 25             # Rows per request
BACKOFF_BASE = 2.0        # Retry delay multiplier (2 → 2s, 4s, 8s…)
MAX_BACKOFF = 60          # Max delay between retries in seconds
# JSON API scraper settings end