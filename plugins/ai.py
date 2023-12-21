# Copyright 2023 Qewertyy, MIT License

from pyrogram import Client, filters, types as t
from Utils import getText,ChatCompletion,getMedia,geminiVision

@Client.on_message(filters.command(["gpt","bard","llama","mistral","palm","gemini"]))
async def chatbots(_: Client,m: t.Message):
    prompt = getText(m)
    media = getMedia(m)
    if media is not None:
        return await askAboutImage(_,m,[media],prompt)
    if prompt is None:
        return await m.reply_text("Hello, How can i assist you today?")
    model = m.command[0].lower()
    output = await ChatCompletion(prompt,model)
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
    await m.reply_text(output)

async def askAboutImage(_:Client,m:t.Message,mediaFiles: list,prompt:str):
    images = []
    for media in mediaFiles:
        image = await _.download_media(media.file_id,file_name=f'./downloads/{m.from_user.id}_ask.jpg')
        images.append(image)
    output = await geminiVision(prompt if prompt else "whats this?","geminiVision",images)
    await m.reply_text(output)