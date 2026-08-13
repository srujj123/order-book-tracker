import asyncio
import sys

from src.order_book import OrderBook
from src.feed_client import stream_order_book
from src.display import render


async def main():
    product_id = sys.argv[1] if len(sys.argv) > 1 else "BTC-USD"
    book = OrderBook()
    await stream_order_book(product_id, book, on_update=render)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nStopped.")