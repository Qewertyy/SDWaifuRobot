# Copyright 2023 Qewertyy, MIT License
import httpx
from urllib.parse import urlsplit
from .pastebins import nekobin
from bot import TelegraphClient


async def evaluateContent(text):
    if len(text) < 4096:
        return text
    link = await nekobin(text)
    link += "\n\n#ERROR"
    return link


async def getFile(message):
    if not message.reply_to_message:
        return None
    if (
        message.reply_to_message.document is False
        or message.reply_to_message.photo is False
    ):
        return None
    if (
        message.reply_to_message.document
        and message.reply_to_message.document.mime_type
        in ["image/png", "image/jpg", "image/jpeg"]
        or message.reply_to_message.photo
    ):
        if (
            message.reply_to_message.document
            and message.reply_to_message.document.file_size > 5242880
        ):
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
    media = (
        message.media
        if message.media
        else message.reply_to_message.media if message.reply_to_message else None
    )
    if message.media:
        if message.photo:
            media = message.photo
        elif (
            message.document
            and message.document.mime_type in ["image/png", "image/jpg", "image/jpeg"]
            and message.document.file_size < 5242880
        ):
            media = message.document
        else:
            media = None
    elif message.reply_to_message and message.reply_to_message.media:
        if message.reply_to_message.photo:
            media = message.reply_to_message.photo
        elif (
            message.reply_to_message.document
            and message.reply_to_message.document.mime_type
            in ["image/png", "image/jpg", "image/jpeg"]
            and message.reply_to_message.document.file_size < 5242880
        ):
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
        imageType = response.headers["content-type"].split("/")[1]
        if imageType == "gif":
            return None
        return response.content
    except (TimeoutError, httpx.ReadTimeout, httpx.ReadError):
        return None


def getContentType(url):
    """Get Media Content Type"""
    try:
        client = httpx.Client()
        response = client.head(url)
        if response.status_code != 200:
            return None
        return response.headers["content-type"].split("/")[0]
    except (TimeoutError, httpx.ReadTimeout, httpx.ReadError):
        return None


def createMessage(platform, data):
    message = ""
    htmlMessage = ""
    if platform == "google":
        names = data["bestResults"]["names"]
        urls = data["bestResults"]["urls"]
        if len(names) > 10:
            message = "\n".join(
                [f"{index+1}. {name}" for index, name in enumerate(names[:10])]
            )
            htmlMessage = f"<br/>".join(
                [f"{index+1}. {name}" for index, name in enumerate(names)]
            )
            htmlMessage += "<br/><br/><h3>URLS</h3><br/>"
            htmlMessage += f"<br/>".join([f"{url}" for url in urls])
            htmlMessage += (
                "<br/><br/>By <a href='https://lexica.qewertyy.dev'>LexicaAPI</a>"
            )
            url = TelegraphClient.createPage("More Results", htmlMessage)
            message += f"\n\n<a href='{url}'>More Results</a>\nBy @LexicaAPI"
        else:
            message = "\n".join(
                [f"{index+1}. {name}" for index, name in enumerate(names)]
            )
    elif platform == "yandex":
        message = "\n".join(
            [
                f"{index+1}. {result['name']}"
                for index, result in enumerate(data["bestResults"])
            ]
        )
        htmlMessage = f"<br/>".join(
            [
                f"{index+1}. <a href=f'{result['url']}'>{result['name']}</a>"
                for index, result in enumerate(data["relatedSearches"])
            ]
        )
        htmlMessage += (
            "<br/><br/>By <a href='https://lexica.qewertyy.dev'>LexicaAPI</a>"
        )
        url = TelegraphClient.createPage("More Results", htmlMessage)
        message += f"\n\n<a href='{url}'>More Results</a>\nBy @LexicaAPI"
    elif platform == "bing":
        if len(data["bestResults"]) > 10:
            message = "\n".join(
                [
                    f"{index+1}. {result['name']}"
                    for index, result in enumerate(data["bestResults"][:10])
                ]
            )
            htmlMessage = "<br/>".join(
                [
                    f"{index+1}. <a href={result['url']}>{result['name']}</a>"
                    for index, result in enumerate(data["bestResults"])
                ]
            )
            htmlMessage += (
                "<br/><br/>By <a href='https://lexica.qewertyy.dev'>LexicaAPI</a>"
            )
            url = TelegraphClient.createPage("More Results", htmlMessage)
            message += f"\n\n<a href='{url}'>More Results</a>\nBy @LexicaAPI"
        else:
            message = "\n".join(
                [
                    f"{index+1}. {result['name']}"
                    for index, result in enumerate(data["bestResults"])
                ]
            )
    return {"message": message, "htmlMessage": htmlMessage}
