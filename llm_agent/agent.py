# llm_agent/agent.py
import os

from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType

from .tools import make_tools


def create_agent(user_id: str):
    """
    Create a LangChain agent configured for a specific user_id.
    """

    # Make sure OPENAI_API_KEY is set in env or .env
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise RuntimeError("OPENAI_API_KEY not set in environment.")

    llm = ChatOpenAI(
        model="gpt-4.1-mini",
        temperature=0,
    )

    tools = make_tools(user_id)

    system_message = """
You are a stock portfolio assistant.
You can:
- record BUY and SELL trades for the user
- show profit for a specific stock
- show total profit across all stocks

When the user describes a trade (e.g. "I bought 10 NVDA at 120"),
call the trade-recording tool with the correct arguments.

When the user asks about profit for a ticker,
use the ticker profit tool.

When the user asks about overall profit or portfolio performance,
use the total profit tool.

Always respond with clear numbers (shares, average cost, current price, P/L).
"""

    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.OPENAI_FUNCTIONS,
        verbose=True,
        agent_kwargs={"system_message": system_message},
    )

    return agent
