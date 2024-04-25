# Copyright 2023 Qewertyy, MIT License

from pyrogram import Client, filters, types as t
from config import Config
from Utils import identifyPlatform,DownloadMedia,getContentType


@Client.on_message(filters.regex(pattern=Config.mediaPattern))
@identifyPlatform
async def media_downloader(_,m: t.Message):
    if m.url is None or m.platform is None:
        return
    output = await DownloadMedia(m.platform,m.url)
    if output is None or output['code'] != 2 :
        return await m.reply_text("Unable to download media.")
    buildMedia = []
    medias = output['content']['mediaUrls'] if 'mediaUrls' in output['content'] else output['content']
    for media in medias:
        if 'type' in media:
            if media['type'] in ["image","photo"]:
                buildMedia.append(t.InputMediaPhoto(media['url']))
            elif media['type'] == "video":
                buildMedia.append(t.InputMediaVideo(media['url']))
        else:
            mediaType = getContentType(media['url'])
            if mediaType in ["image","photo"]:
                buildMedia.append(t.InputMediaPhoto(media['url']))
            elif mediaType == "video":
                buildMedia.append(t.InputMediaVideo(media['url']))
    if len(buildMedia) == 0:
        return await m.reply_text("Unable to download media.")
    await m.reply_media_group(
        buildMedia,
        reply_to_message_id=m.id
    )
    return