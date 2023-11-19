# Copyright 2023 Qewertyy, MIT License

from pyrogram import Client, filters, types as t
from Utils import getText,ChatCompletion

@Client.on_message(filters.command(["gpt","bard","llama","mistral","palm"]))
async def chatbots(_: Client,m: t.Message):
    prompt = getText(m)
    if prompt is None:
        return await m.reply_text("Hello, How can i assist you today?")
    model = m.command[0].lower()
    output = await ChatCompletion(prompt,model)
    if type(output) == output.__class__:
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