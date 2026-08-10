from src.order_book import OrderBook


def test_load_snapshot_populates_bids_and_asks():
    book = OrderBook()
    bids = [["100.50", "1.5"], ["100.25", "2.0"]]
    asks = [["100.75", "1.0"], ["101.00", "3.0"]]

    book.load_snapshot(bids, asks)

    assert book.bids == {100.50: 1.5, 100.25: 2.0}
    assert book.asks == {100.75: 1.0, 101.00: 3.0}


def test_apply_change_adds_new_bid_level():
    book = OrderBook()
    book.apply_change("buy", "100.50", "2.0")

    assert book.bids == {100.50: 2.0}


def test_apply_change_adds_new_ask_level():
    book = OrderBook()
    book.apply_change("sell", "101.00", "3.0")

    assert book.asks == {101.00: 3.0}


def test_apply_change_updates_existing_level():
    book = OrderBook()
    book.apply_change("buy", "100.50", "2.0")
    book.apply_change("buy", "100.50", "5.0")  # same price, new size

    assert book.bids == {100.50: 5.0}


def test_apply_change_with_zero_size_removes_level():
    book = OrderBook()
    book.apply_change("buy", "100.50", "2.0")
    book.apply_change("buy", "100.50", "0")  # size 0 = remove this level

    assert book.bids == {}


def test_apply_change_zero_size_on_missing_level_does_not_error():
    book = OrderBook()
    # removing a level that was never there shouldn't crash
    book.apply_change("sell", "999.00", "0")

    assert book.asks == {}


def test_top_levels_returns_bids_sorted_descending():
    book = OrderBook()
    book.load_snapshot(
        bids=[["100.00", "1.0"], ["102.00", "1.0"], ["101.00", "1.0"]],
        asks=[],
    )

    best_bids, _ = book.top_levels()

    prices = [price for price, size in best_bids]
    assert prices == [102.00, 101.00, 100.00]


def test_top_levels_returns_asks_sorted_ascending():
    book = OrderBook()
    book.load_snapshot(
        bids=[],
        asks=[["102.00", "1.0"], ["100.00", "1.0"], ["101.00", "1.0"]],
    )

    _, best_asks = book.top_levels()

    prices = [price for price, size in best_asks]
    assert prices == [100.00, 101.00, 102.00]


def test_top_levels_respects_depth_limit():
    book = OrderBook()
    bids = [[str(100 + i), "1.0"] for i in range(20)]  # 20 price levels
    book.load_snapshot(bids=bids, asks=[])

    best_bids, _ = book.top_levels(depth=5)

    assert len(best_bids) == 5