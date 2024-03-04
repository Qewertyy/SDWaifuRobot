# Copyright 2024 Qewertyy, MIT License

import os
from dotenv import load_dotenv
load_dotenv()

class Config(object):
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    mediaPattern = r"\b(https?://(?:(.*?)\.)?(?:instagram\.com|www\.instagram\.com|t\.co|twitter\.com|x\.com|pin\.it|pinterest\.com|in\.pinterest\.com)(?:[^\s]*))\b"
    WEBHOOK_HOST = os.getenv("WEBHOOK_HOST")
    TELEGRAM_FILE_URL = "https://api.telegram.org/file/bot"