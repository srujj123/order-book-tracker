"""Logs periodic order book snapshots + engineered features to a CSV for later training."""

import csv
import time
from pathlib import Path

FEATURE_COLUMNS = [
    "timestamp", "mid_price", "spread",
    "bid_volume_top5", "ask_volume_top5", "imbalance",
]


class DataLogger:
    def __init__(self, filepath="data/book_snapshots.csv"):
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        self.filepath = filepath
        self._write_header_if_needed()

    def _write_header_if_needed(self):
        if not Path(self.filepath).exists():
            with open(self.filepath, "w", newline="") as f:
                csv.writer(f).writerow(FEATURE_COLUMNS)

    def log(self, book):
        best_bids, best_asks = book.top_levels(depth=5)
        if not best_bids or not best_asks:
            return

        best_bid, best_ask = best_bids[0][0], best_asks[0][0]
        mid_price = (best_bid + best_ask) / 2
        spread = best_ask - best_bid

        bid_vol = sum(size for _, size in best_bids)
        ask_vol = sum(size for _, size in best_asks)
        imbalance = (bid_vol - ask_vol) / (bid_vol + ask_vol) if (bid_vol + ask_vol) else 0.0

        with open(self.filepath, "a", newline="") as f:
            csv.writer(f).writerow([time.time(), mid_price, spread, bid_vol, ask_vol, imbalance])