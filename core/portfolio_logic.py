# core/portfolio_logic.py
from collections import defaultdict
from datetime import datetime

import yfinance as yf

from .db import transactions_col


# ---------- Basic DB operations ----------

def record_trade(user_id: str, ticker: str, action: str,
                 quantity: float, price: float, fee: float = 0.0):
    """Insert a BUY or SELL transaction into MongoDB."""
    doc = {
        "user_id": user_id,
        "ticker": ticker.upper(),
        "action": action.upper(),  # "BUY" or "SELL"
        "quantity": float(quantity),
        "price": float(price),
        "fee": float(fee),
        "trade_date": datetime.utcnow(),
    }
    transactions_col.insert_one(doc)
    return doc


def get_transactions_for_user(user_id: str):
    """Fetch all transactions for this user."""
    cursor = transactions_col.find({"user_id": user_id})
    return list(cursor)


# ---------- Portfolio math ----------

def compute_positions(transactions):
    """
    Compute per-ticker positions using average-cost method.
    Returns: dict[ticker] -> {shares, avg_cost, realized_pl}
    """
    positions = defaultdict(lambda: {
        "shares": 0.0,
        "avg_cost": 0.0,
        "realized_pl": 0.0
    })

    for tx in transactions:
        ticker = tx["ticker"].upper()
        action = tx["action"].upper()
        qty = float(tx["quantity"])
        price = float(tx["price"])
        fee = float(tx.get("fee", 0.0))

        p = positions[ticker]

        if action == "BUY":
            old_cost = p["shares"] * p["avg_cost"]
            new_cost = qty * price + fee
            total_cost = old_cost + new_cost
            new_shares = p["shares"] + qty

            p["shares"] = new_shares
            p["avg_cost"] = total_cost / new_shares if new_shares != 0 else 0.0

        elif action == "SELL":
            realized = (price - p["avg_cost"]) * qty - fee
            p["realized_pl"] += realized
            p["shares"] -= qty
            if p["shares"] == 0:
                p["avg_cost"] = 0.0

    return positions


def get_current_price(ticker: str) -> float:
    """Get latest close price using yfinance."""
    data = yf.Ticker(ticker)
    hist = data.history(period="1d")
    return float(hist["Close"].iloc[-1])


# ---------- High-level profit helpers for tools ----------

def get_profit_for_ticker(user_id: str, ticker: str) -> dict:
    """Compute realized & unrealized P/L for a single ticker."""
    txs = get_transactions_for_user(user_id)
    txs_for_ticker = [tx for tx in txs if tx["ticker"].upper() == ticker.upper()]

    if not txs_for_ticker:
        return {"error": f"No transactions found for {ticker.upper()}."}

    positions = compute_positions(txs_for_ticker)
    p = positions[ticker.upper()]

    if p["shares"] > 0:
        current_price = get_current_price(ticker)
        market_value = p["shares"] * current_price
        cost_basis = p["shares"] * p["avg_cost"]
        unrealized = market_value - cost_basis
        unrealized_pct = (unrealized / cost_basis * 100) if cost_basis > 0 else 0.0
    else:
        current_price = 0.0
        market_value = 0.0
        unrealized = 0.0
        unrealized_pct = 0.0

    return {
        "ticker": ticker.upper(),
        "shares": p["shares"],
        "avg_cost": p["avg_cost"],
        "current_price": current_price,
        "market_value": market_value,
        "realized_pl": p["realized_pl"],
        "unrealized_pl": unrealized,
        "unrealized_pct": unrealized_pct,
        "total_pl": p["realized_pl"] + unrealized,
    }


def get_total_profit(user_id: str) -> dict:
    """Compute total realized & unrealized P/L across all tickers."""
    txs = get_transactions_for_user(user_id)
    positions = compute_positions(txs)

    by_ticker = {}
    total_realized = 0.0
    total_unrealized = 0.0

    for ticker, p in positions.items():
        if p["shares"] > 0:
            current_price = get_current_price(ticker)
            market_value = p["shares"] * current_price
            cost_basis = p["shares"] * p["avg_cost"]
            unrealized = market_value - cost_basis
            unrealized_pct = (unrealized / cost_basis * 100) if cost_basis > 0 else 0.0
        else:
            current_price = 0.0
            market_value = 0.0
            unrealized = 0.0
            unrealized_pct = 0.0

        total_realized += p["realized_pl"]
        total_unrealized += unrealized

        by_ticker[ticker] = {
            **p,
            "current_price": current_price,
            "market_value": market_value,
            "unrealized_pl": unrealized,
            "unrealized_pct": unrealized_pct,
        }

    return {
        "by_ticker": by_ticker,
        "total_realized": total_realized,
        "total_unrealized": total_unrealized,
        "total_pl": total_realized + total_unrealized,
    }
