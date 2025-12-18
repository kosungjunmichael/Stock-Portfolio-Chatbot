import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

uri = os.getenv("MONGODB_URI")
if not uri:
    raise RuntimeError("MONGODB_URI missing")

client = MongoClient(uri, serverSelectionTimeoutMS=5000)

# Forces a real connection attempt:
client.admin.command("ping")
print("✅ MongoDB connected successfully!")
