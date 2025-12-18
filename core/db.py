# core/db.py
from pymongo import MongoClient

# Adjust the URI if needed (Docker, Atlas, etc.)
client = MongoClient("mongodb://localhost:27017")

db = client["portfolio_db"]
transactions_col = db["transactions"]
