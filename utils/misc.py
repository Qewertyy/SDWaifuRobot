# Copyright 2024 Qewertyy, MIT License

import httpx
from urllib.parse import urlsplit
from .pastebins import nekobin
from config import Config

async def evaluateContent(text):
    if len(text) < 4096:
        return text
    link = await nekobin(text)
    link += "\n\n#ERROR"
    return link

async def getFile(bot,message):
    if not message.reply_to_message:
        return None
    if message.reply_to_message.document is False or message.reply_to_message.photo is False:
        return None
    if message.reply_to_message.document and message.reply_to_message.document.mime_type in ['image/png','image/jpg','image/jpeg'] or message.reply_to_message.photo:
        if message.reply_to_message.document and message.reply_to_message.document.file_size > 5242880:
            return 1
        fileId= message.reply_to_message.photo[-1].file_id if message.reply_to_message.photo else message.reply_to_message.document.file_id
        image = await bot.get_file(fileId)
        imageUrl = Config.TELEGRAM_FILE_URL + Config.BOT_TOKEN + "/" + image.file_path
        return imageUrl
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
            return None
        imageType = response.headers['content-type'].split("/")[1]
        if imageType == "gif":
            return None
        return response.content
    except (TimeoutError, httpx.ReadTimeout,httpx.ReadError):
        return None

def getContentType(url):
    """Get Media Content Type"""
    try:
        client = httpx.Client()
        response = client.head(url)
        if response.status_code != 200:
            return None
        return response.headers['content-type'].split("/")[0]
    except (TimeoutError, httpx.ReadTimeout,httpx.ReadError):
        return None

async def uploadTo0x0st(imageUrl):
    """Upload Image to 0x0st"""
    try:
        client = httpx.Client()
        response = client.post("https://0x0.st",files={"url": imageUrl})
        if response.status_code != 200:
            return None
        output= response.text
        return output
    except (TimeoutError, httpx.ReadTimeout,httpx.ReadError):
        return None

def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time