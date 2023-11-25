from pyrogram import Client, filters, types as t
from Utils import getFile, UpscaleImages
import os

@Client.on_message(filters.command(["upscale"]))
async def upscaleImages(_, message):
    file = await getFile(message)
    if file == 1:
       return await message.reply_text("File size is large")
    if file is None:
       return await message.reply_text("Replay to an image?")
    msg = await message.reply("wait a min...")
    imageBytes = open(file,"rb").read()
    os.remove(file)
    upscaledImage = await UpscaleImages(imageBytes)
    try:
      await message.reply_document(open(upscaledImage,"rb"))
      await msg.delete()
      os.remove(upscaledImage)
    except Exception as e:
       await msg.edit(f"{e}")