import os
from dotenv import load_dotenv

load_dotenv()
PROXY_URL = os.getenv("PROXY_URL")
API_CHAT_URL=str(os.getenv("API_CHAT_URL"))
EMBED_URL=str(os.getenv("EMBED_URL"))
MONGO_URL = os.getenv("MONGO_URL")
MONGO_DB_NAME = str(os.getenv("MONGO_DB_NAME"))
TELEGRAM_TOKEN=os.getenv("TELEGRAM_TOKEN")