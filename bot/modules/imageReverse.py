# Copyright 2024 Qewertyy, MIT License

import traceback
from bot import dp
from aiogram import types, filters
from utils import ReverseImageSearch,getFile,uploadToTelegraph
from bot import TelegraphClient

@dp.message_handler(
    filters.Command(
        commands=["pp","reverse","sauce"], prefixes="!/", ignore_case=False
    )
)
async def reverseImageSearch(m: types.Message):
    try:
        reply = await m.reply("`Downloading...`",parse_mode=types.ParseMode.MARKDOWN)
        file = await getFile(dp.bot,m)
        if file is None:
            return await reply.edit_text("Reply to an image?")
        if file == 1:
            return await reply.edit_text("File size is large")
        await reply.edit_text("`Uploading to the server...`",parse_mode=types.ParseMode.MARKDOWN)
        output = await ReverseImageSearch(file,"google")
        if output['code'] != 2:
            return await reply.edit_text("Ran into an error.")
        message = ''
        names = output['content']['bestResults']['names']
        urls = output['content']['bestResults']['urls']
        if len(names) > 10:
            message = "\n".join([f"{index+1}. {name}" for index, name in enumerate(names[:10])])
            htmlMessage = f"<br/>".join([f"{index+1}. {name}" for index, name in enumerate(names)])
            htmlMessage += "<br/><br/><h3>URLS</h3><br/>"
            htmlMessage += f"<br/>".join([f"{url}" for url in urls])
            htmlMessage += "<br/><br/>By <a href='https://lexica.qewertyy.me'>LexicaAPI</a>"
            url = TelegraphClient.createPage("More Results",htmlMessage)
            message += f"\n\n<a href='{url}'>More Results</a>\nBy @LexicaAPI"
            await reply.delete()
            return await m.reply(message,parse_mode=types.ParseMode.HTML)
        message ="\n".join([f"{index+1}. {name}" for index, name in enumerate(output['content']['bestResults']['names'])])
        await reply.delete()
        await m.reply(f"{message}\n\nBy @LexicaAPI")
    except Exception as E:
        traceback.print_exc()
        return await m.reply("Ran into an error.")