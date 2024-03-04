# Copyright 2024 Qewertyy, MIT License

from bot import dp
from utils import getText,SearchImages,getImageContent
import traceback,random,io
from aiogram import types, filters,exceptions as errors

@dp.message_handler(
    filters.Command(
        commands=["img","image","imagesearch"], prefixes="!/", ignore_case=False
    )
)
async def searchImages(m: types.Message):
    try:
        reply = await m.reply("`Searching...`",parse_mode=types.ParseMode.MARKDOWN)
        prompt = getText(m)
        if prompt is None:
            return await reply.edit_text("What do you want to search?")
        output = await SearchImages(prompt,"google")
        if output['code'] != 2:
            return await reply.edit_text("Ran into an error.")
        images = output['content']
        if len(images) == 0:
            return await reply.edit_text("No results found.")
        images = random.choices(images,k=8 if len(images) > 8 else len(images))
        media = []
        for image in images:
            content = getImageContent(image['imageUrl'])
            if content is None:
                images.remove(image)
                continue
            else:
                media.append(types.InputMediaPhoto(types.InputFile(io.BytesIO(content))))
        await m.reply_media_group(
            media
            )
        await reply.delete()
    except (errors.InvalidHTTPUrlContent):
        return await reply.edit("Ran into an error.")
    except Exception as e:
        traceback.print_exc()
        return await reply.edit("Ran into an error.")