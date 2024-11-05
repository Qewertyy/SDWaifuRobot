import os
from dotenv import load_dotenv
load_dotenv()

class Config(object):
    DB_NAME = os.getenv("DB_NAME")
    DB_HOST = os.getenv("DB_HOST")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    API_ID = os.getenv("API_ID")
    API_HASH = os.getenv("API_HASH")
    mediaPattern = r"\b(https?://(?:(.*?)\.)?(?:instagram\.com|www\.instagram\.com|t\.co|twitter\.com|x\.com|pin\.it|pinterest\.com|in\.pinterest\.com)(?:[^\s]*))\b"
    BOT_ID = int(os.getenv("BOT_TOKEN").split(":")[0])