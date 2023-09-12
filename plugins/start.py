# Copyright 2023 Qewertyy, MIT License

from pyrogram import Client, filters, types as t
from bot import StartTime

@Client.on_message(filters.command(["start","help","repo"]))
async def start(_: Client, m: t.Message):
    await m.reply_text(
        "Just an image generation bot by @Qewertyy.\n\nCommands: \n`/draw`: create images\n`/upscale`: upscale your images",
        reply_markup=t.InlineKeyboardMarkup(
            [
                [
                    t.InlineKeyboardButton(text="Source",url="https://github.com/Qewertyy/SDWaifuRobot")
                ]
            ]
        )
    )
