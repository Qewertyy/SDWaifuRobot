# Copyright 2023 Qewertyy, MIT License

import uvloop
import datetime,logging, sys
from pyrogram import Client
from lexica import Client as ApiClient
from lexica.constants import version
from config import Config
from Utils.telegraph import GraphClient

# Get logging configurations
logging.basicConfig(
    format="%(asctime)s - [BOT] - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("logs.txt"), logging.StreamHandler()],
    level=logging.INFO,
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)
LOGGER = logging.getLogger(__name__)

StartTime = datetime.datetime.now()
Models = ApiClient().models['models']['image']
LOGGER.info(f"Models Loaded: v{version}")

db = {}

TelegraphClient = GraphClient(
    "LexicaAPI",
    "https://t.me/LexicaAPI",
    "LexicaAPI"
).createAccount()

class Bot(Client):
    def __init__(self):
        super().__init__(
            "SDWaifuRobot",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            plugins=dict(root="plugins"),
        )
        self.models = Models
        self.db = db
        if not self.models:
            LOGGER.error("Models are empty!")
            sys.exit(1)

    async def start(self):
        await super().start()
        LOGGER.info("Bot Started")


    async def stop(self):
        self.db.clear()
        await super().stop()
        LOGGER.info("Stopped Services")

if __name__ == "__main__":
    uvloop.install()
    Bot().run()