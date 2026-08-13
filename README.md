# Order Book Tracker

A live order book reconstruction system for Coinbase's public WebSocket feed, with an in-progress
machine learning component for short-horizon price movement prediction.

Built as a portfolio project to explore real-time data processing, distributed-systems-style
message handling, and the kind of high-throughput market data work seen in trading infrastructure
and data engineering roles.

## What it does

- Connects to Coinbase's public `level2_batch` WebSocket channel (no API key required)
- Reconstructs a full local order book from an initial snapshot + incremental updates
- Renders the live top-of-book (best bids/asks, spread) to the terminal, refreshed in real time
- Logs periodic order book snapshots + engineered features (spread, volume imbalance) to CSV,
  building a dataset for a downstream ML model that predicts short-term mid-price movement

## Why it's structured this way

The project is deliberately split into single-responsibility modules rather than one script:

- `src/order_book.py` — pure state management. No networking, no I/O. This means the core book
  logic (applying updates, tracking price levels) can be fully unit tested without a live
  connection.
- `src/feed_client.py` — owns the WebSocket connection and message parsing. Knows nothing about
  how the book is displayed or logged — it just applies updates and calls a callback.
- `src/display.py` — terminal rendering, throttled independently so redraws don't flood the screen.
- `src/data_logger.py` — periodic feature logging for the ML pipeline, throttled separately from
  rendering.

Keeping these decoupled means each piece can change independently — e.g., swapping the terminal
display for a web dashboard, or the exchange feed for a different one, wouldn't require touching
the order book logic at all.

## Running it

```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

pip install -r requirements.txt
python main.py BTC-USD
```

Swap `BTC-USD` for any valid Coinbase product ID.

## Running the tests

```bash
pytest
```

Tests cover snapshot loading, incremental update handling (including zero-size removals and
updates to non-existent levels), and price-level sorting — the core logic that determines whether
the book stays accurate under real, messy feed conditions.



## Status / next steps

- [x] Live order book reconstruction
- [x] Unit test coverage for core book logic
