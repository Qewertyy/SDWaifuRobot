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
    output = await bard(prompt)
    await m.reply_text(output)