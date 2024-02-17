# Copyright 2023 Qewertyy, MIT License

import uvloop
uvloop.install()
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
Models = ApiClient().models
LOGGER.info(f"Models Loaded: v{version}")

TelegraphClient = GraphClient(
    "LexicaAPI",
    "https://t.me/LexicaAPI",
    "LexicaAPI"
)
TelegraphClient.createAccount()

class Bot(Client):
    global StartTime,Models
    #print(Models)
    def __init__(self):
        super().__init__(
            "SDWaifuRobot",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            plugins=dict(root="plugins"),
        )
    async def start(self):
        await super().start()
        LOGGER.info("Bot Started")

    if Models is None:
        LOGGER.error("Models are empty!")
        sys.exit(1)

    async def stop(self):
        await super().stop()
        LOGGER.info("Stopped Services")

if __name__ == "__main__":
    Bot().run()