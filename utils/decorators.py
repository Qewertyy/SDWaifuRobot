# Copyright 2024 Qewertyy, MIT License

from functools import wraps
import traceback,sys,re
from config import Config
from .misc import evaluateContent
from urllib.parse import urlsplit

def errorHandler(func):
    @wraps(func)
    async def wrapper(client, message, *args, **kwargs):
        try:
            await func(client, message, *args, **kwargs)
        except Exception as err:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            errors = traceback.format_exception(
                exc_type,
                exc_obj,
                exc_tb,
            )
            errors = await evaluateContent(
                "#ERROR | `{}` | `{}`\n\n`{}`\n```{}```\n".format(
                    0 if not message.from_user else message.from_user.id,
                    0 if not message.chat else message.chat.id,
                    message.caption if message.caption else message.text,
                    "".join(errors),
                ),
            )
            await client.send_message(Config.LOG_CHANNEL, errors)
            raise err
    return wrapper

def identifyPlatform(func):
    @wraps(func)
    async def wrapper(message, *args, **kwargs):
        url = re.findall(Config.mediaPattern,message.text)[0][0]
        platform = urlsplit(url).netloc.split('.')[-2]
        await func(url,"pinterest" if platform  == "pin" else platform,message, *args, **kwargs)
    return wrapper