# Copyright 2023 Qewertyy, MIT License

from pyrogram import Client, filters, types as t
from bot import StartTime

@Client.on_message(filters.command("start"))
async def start(_: Client, m: t.Message):
    await m.reply_text("Just an image generation bot for free by @Qewertyy.")