# API Configuration
CURRENCY = "bitcoin"
VS_CURRENCY = "usd"
COINGECKO_API_URL = (
    f"https://api.coingecko.com/api/v3/simple/price"
f"?ids={CURRENCY}&vs_currencies={VS_CURRENCY}&include_last_updated_at=true"
)
# Polling Settings
POLL_INTERVAL = 1  # seconds between each API call
SMA_WINDOW = 10    # number of recent prices to average

# Retry Settings
MAX_RETRIES = 5         # maximum number of retries before skipping
INITIAL_BACKOFF = 1     # starting backoff duration in seconds

# Logging Format
LOG_FORMAT = "[%(asctime)s] %(message)s"
DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"