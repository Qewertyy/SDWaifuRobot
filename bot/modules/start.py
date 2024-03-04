# Copyright 2024 Qewertyy, MIT License

from bot import dp,startTime
from aiogram import types, filters
from utils.misc import get_readable_time
import time

startText = """
Just an AI/Utility bot by `@Qewertyy`.

Commands:
`/draw`: create images
`/upscale`: upscale your images
`/gpt`: chatgpt
`/bard`: bard ai by google
`/mistral`: mistral ai
`/llama`: llama by meta ai
`/palm`: palm by google
`/reverse`: reverse image search
`/gemini`: gemini by google

Uptime: `{}`
"""

btns = [
    {
        "text":"Source","url":"https://github.com/Qewertyy/SDWaifuRobot"
    },
    {
        "text":"Deploy to Heroku","url":"https://dashboard.heroku.com/new?template=https://github.com/Qewertyy/SDWaifuRobot"
    }
]

@dp.message_handler(
    filters.Command(
        commands=["start", "help", "repo", "source"], prefixes="!/", ignore_case=False
    )
)
async def start(message: types.Message):
    uptime = get_readable_time((time.time() - startTime))
    markup = types.InlineKeyboardMarkup()
    for btn in btns:
        markup.row(types.InlineKeyboardButton(text=btn['text'], url=btn['url']))
        markup.row_width = 1
    await message.answer(
        startText.format(uptime), parse_mode=types.ParseMode.MARKDOWN, reply_markup=markup
    )
