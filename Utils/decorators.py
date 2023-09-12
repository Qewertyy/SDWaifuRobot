from functools import wraps

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
            errors = evaluateContent(
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