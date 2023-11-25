# Copyright 2023 Qewertyy, MIT License
import traceback
from pyrogram import Client, filters, types as t
from Utils import ReverseImageSearch,getFile,uploadToTelegraph

@Client.on_message(filters.command(["pp","reverse","sauce"]))
async def reverseImageSearch(_: Client,m: t.Message):
    try:
        file = await getFile(m)
        if file == 1:
            return await m.reply_text("File size is large")
        if file is None:
            return await m.reply_text("Reply to an image?")
        imgUrl = await uploadToTelegraph(file)
        if imgUrl is None:
            return await m.reply_text("Ran into an error.")
        output = await ReverseImageSearch("google",imgUrl)
        if output['code'] != 2:
            return await m.reply_text("Ran into an error.")
        message = "\n".join([f"{index+1}. {name}" for index, name in enumerate(output['content']['bestResults']['names'])])
        await m.reply_text(message)
    except Exception as E:
        traceback.print_exc()
        return await m.reply_text("Ran into an error.")