# Copyright 2023 Qewertyy, MIT License

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
    text_to_return = message.text
    if message.text is None:
        return None
    if " " in text_to_return:
        try:
            return message.text.split(None, 1)[1]
        except IndexError:
            return None
    else:
        return None