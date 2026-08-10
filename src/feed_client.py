"""Connects to Coinbase's public WebSocket feed and streams order book updates."""

import json

import websockets

from src.order_book import OrderBook

WS_URI = "wss://ws-feed.exchange.coinbase.com"


async def stream_order_book(product_id, book: OrderBook, on_update=None):
    """
    Connects, subscribes, and applies incoming messages to `book`.
    Calls on_update(product_id, book) after each processed message, if provided
    (this is how main.py plugs in the renderer without feed_client needing
    to know anything about display).
    """
    subscribe_msg = {
        "type": "subscribe",
        "product_ids": [product_id],
        "channels": ["level2_batch"],
    }

    async with websockets.connect(WS_URI, ping_interval=20, max_size=16 * 1024 * 1024) as ws:
        await ws.send(json.dumps(subscribe_msg))

        async for raw in ws:
            msg = json.loads(raw)
            msg_type = msg.get("type")

            if msg_type == "snapshot":
                book.load_snapshot(msg["bids"], msg["asks"])
            elif msg_type == "l2update":
                for side, price, size in msg["changes"]:
                    book.apply_change(side, price, size)
            elif msg_type == "error":
                print("Error from Coinbase feed:", msg)
                continue
            else:
                continue  # subscription confirmations, heartbeats, etc.

            if on_update:
                on_update(product_id, book)