Stock Portfolio Chatbot

This Python-based project is a command-line stock portfolio chatbot that allows users to record BUY and SELL trades and query portfolio performance using natural language. Trades are stored in MongoDB, live market prices are retrieved with yfinance, and profit and loss is calculated using average-cost accounting.

A lightweight LLM agent is used only to interpret user intent and route commands. All financial calculations are handled explicitly in code to ensure correctness and reproducibility.

What This Project Does

You enter a trade or portfolio question in natural language.

The system records trades as transactions in MongoDB.

It retrieves live market prices when needed.

It calculates realized and unrealized profit using average-cost logic.

It returns per-stock or total portfolio results.

All interactions run locally from the terminal using Python.

Example Usage
I bought 10 NVDA at 120
I sold 3 NVDA at 150
What's my profit on NVDA?
What's my total portfolio profit?

Project Structure
portfolio_bot/
│
├── main.py
├── llm_agent/
│   ├── agent.py
│   └── tools.py
├── core/
│   ├── db.py
│   ├── portfolio_logic.py
│   └── __init__.py
└── requirements.txt

Requirements

Python 3.9+

MongoDB (local or remote)

pip (Python package manager)

Python libraries used:

langchain

openai

yfinance

pymongo

pandas

numpy

python-dotenv

All dependencies are listed in requirements.txt.

Installation

From the project root:

pip install -r requirements.txt
python main.py


Ensure MongoDB is running and accessible via the configured URI.

Environment Configuration

Create a .env file in the project root:

OPENAI_API_KEY=your_openai_api_key
MONGO_URI=mongodb://localhost:27017
LLM_MODEL=gpt-4.1-mini


The .env file is excluded from version control.