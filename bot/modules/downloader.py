# Copyright 2024 Qewertyy, MIT License

from aiogram import types, filters
from bot import dp
from config import Config
from utils import identifyPlatform, DownloadMedia, getContentType

caption = "Powered By @LexicaAPI"

@dp.message_handler(filters.Regexp(Config.mediaPattern))
@identifyPlatform
async def media_downloader(url, platform, m: types.Message):
    if url is None or platform is None:
        return
    output = await DownloadMedia(platform, url)
    if output is None or output["code"] != 2:
        return
    buildMedia = []
    for index, media in enumerate(output["content"]):
        mediaType = None
        if "type" in media:
            mediaType = media["type"]
        else:
            mediaType = getContentType(media["url"])
        mediaItem = None
        if mediaType in ["image", "photo"]:
            mediaItem = types.InputMediaPhoto(
                media["url"], caption=caption if index == 0 else None
            )
        elif mediaType == "video":
            mediaItem = types.InputMediaVideo(
                media["url"], caption=caption if index == 0 else None
            )
        else:
            continue
    buildMedia.append(mediaItem)
    if len(buildMedia) == 0:
        return
    await m.reply_media_group(buildMedia)
    return
