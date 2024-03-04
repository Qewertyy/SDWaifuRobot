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

*this [instance](https://sdwaifurobot.vercel.app/) is working on serverless functions*
"""

btns = [
    {
        "text":"Source","url":"https://github.com/Qewertyy/SDWaifuRobot"
    },
    {
        "text":"Deploy to Heroku","url":"https://dashboard.heroku.com/new?template=https://github.com/Qewertyy/SDWaifuRobot"
    },
    {
        "text":"Deploy to Vercel","url":"https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2FQewertyy%2FSDWaifuRobot%2Ftree%2Faiogram&env=BOT_TOKEN,PORT,WEBHOOK_HOST,BOT_TOKEN"
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
