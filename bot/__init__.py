# Copyright 2023 Qewertyy, MIT License

import logging
from urllib.parse import urljoin
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
import time,logging, sys
from lexica import Client as ApiClient
from lexica.constants import version
from config import Config
from utils.telegraph import GraphClient

# Get logging configurations
logging.basicConfig(
    format="%(asctime)s - [BOT] - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
    level=logging.INFO,
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)
LOGGER = logging.getLogger(__name__)

startTime = time.time()
Models = ApiClient().models['models']['image']
LOGGER.info(f"Models Loaded: v{version}")

TelegraphClient = GraphClient(
    "LexicaAPI",
    "https://t.me/LexicaAPI",
    "LexicaAPI"
)
TelegraphClient.createAccount()


WEBHOOK_PATH = f"/api/bot/{Config.BOT_TOKEN}"
WEBHOOK_URL = urljoin(Config.WEBHOOK_HOST, WEBHOOK_PATH)
ALLOWED_UPDATES = ["message", "callback_query", "inline_query"]

client = Bot(token=Config.BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(client, storage=storage)
dp.middleware.setup(LoggingMiddleware())