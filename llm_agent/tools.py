# llm_agent/tools.py
from datetime import datetime

from langchain.tools import tool

from core.portfolio_logic import (
    record_trade,
    get_profit_for_ticker,
    get_total_profit,
)


def make_tools(user_id: str):
    """
    Create tool functions bound to a specific user_id.
    """

    @tool
    def record_trade_tool(ticker: str, action: str, quantity: float,
                          price: float, fee: float = 0.0):
        """Record a BUY or SELL trade for this user."""
        doc = record_trade(
            user_id=user_id,
            ticker=ticker,
            action=action,
            quantity=quantity,
            price=price,
            fee=fee,
        )
        return {
            "status": "ok",
            "ticker": doc["ticker"],
            "action": doc["action"],
            "quantity": doc["quantity"],
            "price": doc["price"],
            "fee": doc["fee"],
            "trade_date": doc["trade_date"].isoformat(),
        }

    @tool
    def get_profit_for_ticker_tool(ticker: str):
        """Get profit summary for a single ticker."""
        return get_profit_for_ticker(user_id=user_id, ticker=ticker)

    @tool
    def get_total_profit_tool():
        """Get total profit across all tickers."""
        return get_total_profit(user_id=user_id)

    return [record_trade_tool, get_profit_for_ticker_tool, get_total_profit_tool]
