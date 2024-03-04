# Copyright 2023 Qewertyy, MIT License

from bot import dp
from aiogram import types, filters
from utils import getText,ChatCompletion,getMedia,geminiVision
from lexica.constants import languageModels

@dp.message_handler(
    filters.Command(
        commands=[i for i in dir(languageModels) if not i.startswith("__")]
        )
)
async def chatbots(m: types.Message):
    prompt = getText(m)
    if prompt is None:
        return await m.reply("Hello, How can i assist you today?")
    model = m.text.split("/")[1].split(" ")[0].lower()
    output = await ChatCompletion(prompt,model)
    if model == "bard":
        output, images = output
        if len(images) == 0:
            return await m.reply(output)
        media = []
        for i in images:
            media.append(t.InputMediaPhoto(i))
        media[0] = types.InputMediaPhoto(images[0],caption=output)
        await m.reply_media_group(
            media
            )
        return
    await m.reply(output['parts'][0]['text'] if model=="gemini" else output)