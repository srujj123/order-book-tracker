"""Maintains a local copy of the order book from a snapshot + incremental l2updates."""

DEPTH = 12  # how many price levels to expose on each side


class OrderBook:
    def __init__(self):
        self.bids = {}  # price(float) -> size(float)
        self.asks = {}

    def load_snapshot(self, bids, asks):
        self.bids = {float(p): float(s) for p, s in bids}
        self.asks = {float(p): float(s) for p, s in asks}

    def apply_change(self, side, price, size):
        price, size = float(price), float(size)
        book = self.bids if side == "buy" else self.asks
        if size == 0.0:
            book.pop(price, None)
        else:
            book[price] = size

    def top_levels(self, depth=DEPTH):
        best_bids = sorted(self.bids.items(), key=lambda x: -x[0])[:depth]
        best_asks = sorted(self.asks.items(), key=lambda x: x[0])[:depth]
        return best_bids, best_asks