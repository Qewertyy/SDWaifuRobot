# Copyright 2023 Qewertyy, MIT License
import traceback
from pyrogram import Client, filters, types as t
from Utils import ReverseImageSearch,getFile,uploadToTelegraph
from bot import TelegraphClient

@Client.on_message(filters.command(["pp","reverse","sauce"]))
async def reverseImageSearch(_: Client,m: t.Message):
    try:
        reply = await m.reply_text("`Downloading...`")
        file = await getFile(m)
        if file is None:
            return await reply.edit("Reply to an image?")
        if file == 1:
            return await reply.edit("File size is large")
        imgUrl = await uploadToTelegraph(file)
        if imgUrl is None:
            return await reply.edit("Ran into an error.")
        output = await ReverseImageSearch("google",imgUrl)
        if output['code'] != 2:
            return await reply.edit("Ran into an error.")
        message = ''
        names = output['content']['bestResults']['names']
        urls = output['content']['bestResults']['urls']
        btn = t.InlineKeyboardMarkup(
            [
                [
                    t.InlineKeyboardButton(text="Image URL",url=urls[-1])
                ]
            ])
        if len(names) > 10:
            message = "\n".join([f"{index+1}. {name}" for index, name in enumerate(names[:10])])
            htmlMessage = f"<br/>".join([f"{index+1}. {name}" for index, name in enumerate(names)])
            htmlMessage += "<br/><br/><h3>URLS</h3><br/>"
            htmlMessage += f"<br/>".join([f"{url}" for url in urls])
            htmlMessage += "<br/><br/>By <a href='https://lexica.qewertyy.me'>LexicaAPI</a>"
            url = TelegraphClient.createPage("More Results",htmlMessage)
            message += f"\n\n[More Results]({url})\nBy @LexicaAPI"
            await reply.delete()
            return await m.reply_text(message,reply_markup=btn)
        message ="\n".join([f"{index+1}. {name}" for index, name in enumerate(output['content']['bestResults']['names'])])
        await reply.delete()
        await m.reply_text(f"{message}\n\nBy @LexicaAPI",reply_markup=btn)
    except Exception as E:
        traceback.print_exc()
        return await m.reply_text("Ran into an error.")