import os
from dotenv import load_dotenv
load_dotenv()

class Config(object):
    BOT_TOKEN = os.getenv("BOT_TOKEN", "6951958770:AAEyTj58WQWRUZ9G2wMT1uhpmI9_OVvN6WE")
    API_ID = os.getenv("API_ID" , "23237740")
    API_HASH = os.getenv("API_HASH", "690d9c8bc9a28338d59216e3ea0501c4")
    mediaPattern = r"\b(https?://(?:(.*?)\.)?(?:instagram\.com|www\.instagram\.com|t\.co|twitter\.com|x\.com|pin\.it|pinterest\.com|in\.pinterest\.com)(?:[^\s]*))\b"
