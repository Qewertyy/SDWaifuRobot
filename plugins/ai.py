# Copyright 2023 Qewertyy, MIT License

from pyrogram import Client, filters, types as t
from Utils import getText,bard,gpt

@Client.on_message(filters.command(["gpt"]))
async def chatgpt(_: Client,m: t.Message):
    prompt = getText(m)
    if prompt is None:
        return await m.reply_text("Hello, How can i assist you today?")
    output = await gpt(prompt)
    await m.reply_text(output)

@Client.on_message(filters.command(["bard"]))
async def bardai(_: Client,m: t.Message):
    prompt = getText(m)
    if prompt is None:
        return await m.reply_text("Hello, How can i assist you today?")
    output,images = await bard(prompt)
    if len(images) == 0:
        await m.reply_text(output)
    else:
        media = []
        for i in images:
            media.append(types.InputMediaPhoto(i))
        media[0] = types.InputMediaPhoto(images[0],caption=text)
        await app.send_media_group(
            message.chat.id,
            media,
            reply_to_message_id=message.id
            )