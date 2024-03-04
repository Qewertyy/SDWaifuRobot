# Copyright 2024 Qewertyy, MIT License

from bot import dp
from aiogram import types, filters
from utils import getFile, UpscaleImages
import traceback

@dp.message_handler(
    filters.Command(
        commands=["upscale"], prefixes="!/", ignore_case=False
    )
)
async def upscaleImages(message: types.Message):
    msg = await message.reply("wait a min...")
    file = await getFile(dp.bot,message)
    if file == 1:
       return await msg.edit_text("File size is large")
    if file is None:
       return await msg.edit_text("Reply to an image?")
    image_url = await UpscaleImages(image_url=file,format="url")
    try:
      await message.reply_document(image_url)
      await msg.delete()
    except Exception as e:
       traceback.print_exc()
       await msg.edit_text("Ran into an error")