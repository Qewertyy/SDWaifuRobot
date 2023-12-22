# Copyright 2023 Qewertyy, MIT License
import httpx
from urllib.parse import urlsplit

async def getFile(message):
    if not message.reply_to_message:
        return None
    if message.reply_to_message.document is False or message.reply_to_message.photo is False:
        return None
    if message.reply_to_message.document and message.reply_to_message.document.mime_type in ['image/png','image/jpg','image/jpeg'] or message.reply_to_message.photo:
        if message.reply_to_message.document and message.reply_to_message.document.file_size > 5242880:
            return 1
        image = await message.reply_to_message.download()
        return image
    else:
        return None

def getText(message):
    """Extract Text From Commands"""
    text_to_return = message.caption if message.caption else message.text
    if message.text is None:
        return None
    if " " in text_to_return:
        try:
            return message.text.split(None, 1)[1]
        except IndexError:
            return None
    else:
        return None
    
def getMedia(message):
    """Extract Media"""
    media = message.media if message.media else message.reply_to_message.media if message.reply_to_message else None
    if message.media:
        if message.photo:
            media = message.photo
        elif message.document and message.document.mime_type in ['image/png','image/jpg','image/jpeg'] and message.document.file_size < 5242880:
            media = message.document
        else:
            media = None
    elif message.reply_to_message and message.reply_to_message.media:
        if message.reply_to_message.photo:
            media = message.reply_to_message.photo
        elif message.reply_to_message.document and message.reply_to_message.document.mime_type in ['image/png','image/jpg','image/jpeg'] and message.reply_to_message.document.file_size < 5242880:
            media = message.reply_to_message.document
        else:
            media = None
    else:
        media = None
    return media

def cleanUrl(url):
    newUrl = urlsplit(url)
    return f"{newUrl.scheme}://{newUrl.netloc}{newUrl.path}"

def getImageContent(url):
    """Get Image Content"""
    try:
        client = httpx.Client()
        response = client.get(cleanUrl(url))
        if response.status_code != 200:
            return None,None
        imageType = response.headers['content-type'].split("/")[1]
        if imageType == "svg+xml":
            return None,None
        if imageType == "octet-stream":
            imageType = "webp"
        if imageType == "gif":
            return None,None
        return response.content,imageType
    except (TimeoutError, httpx.ReadTimeout,httpx.ReadError):
        return None,None