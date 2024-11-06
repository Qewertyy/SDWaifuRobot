# Copyright 2023 Qewertyy, MIT License

from pyrogram import Client, filters, types as t, enums
from Utils import URLS, startText
from database import user_exists, add_user


@Client.on_message(filters.command(["start", "help", "repo", "source"]))
async def start(_: Client, m: t.Message):
    user_id = m.from_user.id
    if m.chat.type == enums.ChatType.PRIVATE and not user_exists(user_id):
        await add_user(user_id, m.from_user.first_name, m.from_user.username)
    await m.reply_text(
        startText,
        reply_markup=t.InlineKeyboardMarkup(
            [[t.InlineKeyboardButton(text="Source", url=URLS.get("GITHUB"))]]
        ),
    )
