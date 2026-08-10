import asyncio
import sys
import time

from src.order_book import OrderBook
from src.feed_client import stream_order_book
from src.display import render
from src.data_logger import DataLogger

LOG_INTERVAL = 1.0  # seconds - how often to write a row to the CSV


def make_on_update(logger):
    """Returns a callback that renders every update but only logs once per LOG_INTERVAL."""
    last_log_time = [0.0]  # mutable container so the closure can update it

    def on_update(product_id, book):
        render(product_id, book)

        now = time.monotonic()
        if now - last_log_time[0] >= LOG_INTERVAL:
            logger.log(book)
            last_log_time[0] = now

    return on_update


async def main():
    product_id = sys.argv[1] if len(sys.argv) > 1 else "BTC-USD"
    book = OrderBook()
    logger = DataLogger()
    on_update = make_on_update(logger)

    await stream_order_book(product_id, book, on_update=on_update)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nStopped.")