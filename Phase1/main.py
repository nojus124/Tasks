# main.py

import signal
import sys

from crawler.scheduler import Scheduler
from config import (
    COINGECKO_API_URL,
    POLL_INTERVAL,
    SMA_WINDOW,
    MAX_RETRIES,
    INITIAL_BACKOFF,
)


def main():
    # Create the scheduler (orchestrator)
    scheduler = Scheduler(
        url=COINGECKO_API_URL,
        poll_interval=POLL_INTERVAL,
        sma_window=SMA_WINDOW,
        max_retries=MAX_RETRIES,
        initial_backoff=INITIAL_BACKOFF,
    )

    # Define clean shutdown behavior on Ctrl+C
    def shutdown_handler(sig, frame):
        print("\nShutting down…")
        scheduler.shutdown()
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown_handler)

    # Start the main polling loop
    scheduler.run()


if __name__ == "__main__":
    main()
