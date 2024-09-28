# Copyright 2023 Qewertyy, MIT License

from pyrogram import Client, filters, types as t
from Utils import URLS, startText

@Client.on_message(filters.command(["start","help","repo","source"]))
async def start(_: Client, m: t.Message):
    await m.reply_text(
        startText,
        reply_markup=t.InlineKeyboardMarkup(
            [
                [
                    t.InlineKeyboardButton(text="Source",url=URLS.get('GITHUB'))
                ]
            ]
        )
    )
