"""Terminal rendering for a live order book."""

import time

from src.order_book import DEPTH

RENDER_INTERVAL = 0.15  # seconds - throttle redraws
_last_render = [0.0]  # mutable container so we can track state across calls


def clear_screen():
    print("\x1b[2J\x1b[H", end="")


def render(product_id, book):
    now = time.monotonic()
    if now - _last_render[0] < RENDER_INTERVAL:
        return
    _last_render[0] = now

    best_bids, best_asks = book.top_levels()
    clear_screen()

    best_bid = best_bids[0][0] if best_bids else 0.0
    best_ask = best_asks[0][0] if best_asks else 0.0
    spread = best_ask - best_bid if (best_bid and best_ask) else 0.0

    print(f"{product_id}  |  spread: {spread:.2f}  |  {time.strftime('%H:%M:%S')}")
    print("-" * 46)
    print(f"{'BID SIZE':>12} {'BID PRICE':>12} | {'ASK PRICE':<12} {'ASK SIZE':<12}")
    print("-" * 46)

    for i in range(DEPTH):
        bid = best_bids[i] if i < len(best_bids) else None
        ask = best_asks[i] if i < len(best_asks) else None
        bid_str = f"{bid[1]:>12.4f} {bid[0]:>12.2f}" if bid else f"{'':>12} {'':>12}"
        ask_str = f"{ask[0]:<12.2f} {ask[1]:<12.4f}" if ask else f"{'':<12} {'':<12}"
        print(f"{bid_str} | {ask_str}")