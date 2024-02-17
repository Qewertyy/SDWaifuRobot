import os
from dotenv import load_dotenv
load_dotenv()

class Config(object):
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    API_ID = os.getenv("API_ID")
    API_HASH = os.getenv("API_HASH")
    mediaPattern = r"\b(https?://(?:(.*?)\.)?(?:instagram\.com|www\.instagram\.com|t\.co|twitter\.com|x\.com|pin\.it|pinterest\.com|in\.pinterest\.com)(?:[^\s]*))\b"