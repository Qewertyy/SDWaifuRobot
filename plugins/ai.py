# Copyright 2023 Qewertyy, MIT License

from pyrogram import Client, filters, types as t
from Utils import getText,ChatCompletion,getMedia,geminiVision,filter_replies_to_bot
from lexica.constants import languageModels
from config import Config
from database import clear_history

@Client.on_message(filter_replies_to_bot(Config.BOT_ID))
async def chat(_: Client,m: t.Message):
    prompt = m.text
    if prompt is None:
        return await m.reply_text("Hello, How can i assist you today?")
    output = await ChatCompletion(m.from_user.id,m.from_user.first_name,prompt,"gpt")
    await m.reply_text(output)


@Client.on_message(filters.command([i for i in dir(languageModels) if not i.startswith("__")]))
async def chatbots(_: Client,m: t.Message):
    prompt = getText(m)
    media = getMedia(m)
    if media is not None:
        return await askAboutImage(_,m,[media],prompt)
    if prompt is None:
        return await m.reply_text("Hello, How can i assist you today?")
    model = m.command[0].lower()
    output = await ChatCompletion(m.from_user.id,m.from_user.first_name,prompt,model)
    if model == "bard":
        output, images = output
        if len(images) == 0:
            return await m.reply_text(output)
        media = []
        for i in images:
            media.append(t.InputMediaPhoto(i))
        media[0] = t.InputMediaPhoto(images[0],caption=output)
        await _.send_media_group(
            m.chat.id,
            media,
            reply_to_message_id=m.id
            )
        return
    await m.reply_text(output[0]['text'] if model=="gemini" else output)

async def askAboutImage(_:Client,m:t.Message,mediaFiles: list,prompt:str):
    images = []
    for media in mediaFiles:
        image = await _.download_media(media.file_id,file_name=f'./downloads/{m.from_user.id}_ask.jpg')
        images.append(image)
    output = await geminiVision(prompt if prompt else "whats this?","geminiVision",images)
    await m.reply_text(output)


@Client.on_message(filters.command(["clear_history","clear"]))
async def delete_chat_history(_: Client,m: t.Message):
    await clear_history(m.from_user.id)
    await m.reply_text("History cleared.")