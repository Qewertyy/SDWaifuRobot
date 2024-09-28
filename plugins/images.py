# Copyright 2023 Qewertyy, MIT License

from pyrogram import Client, filters, types as t,errors
from Utils import getText,SearchImages,getImageContent,getFile,upload
import traceback,random,io

@Client.on_message(filters.command(["img","image","imagesearch"]))
async def searchImages(_: Client,m:t.Message):
    try:
        reply = await m.reply_text("`Searching...`")
        prompt = getText(m)
        if prompt is None:
            return await reply.edit("What do you want to search?")
        output = await SearchImages(prompt,"google")
        if output['code'] != 2:
            return await reply.edit("Ran into an error.")
        images = output['content']
        if len(images) == 0:
            return await reply.edit("No results found.")
        images = random.choices(images,k=8 if len(images) > 8 else len(images))
        media = []
        for image in images:
            content = getImageContent(image['imageUrl'])
            if content is None:
                images.remove(image)
                continue
            else:
                media.append(t.InputMediaPhoto(io.BytesIO(content)))
        await m.reply_media_group(
            media,
            quote=True
            )
        await reply.delete()
    except (errors.ExternalUrlInvalid, errors.WebpageCurlFailed,errors.WebpageMediaEmpty) as e:
        print(e)
        return await reply.edit("Ran into an error.")
    except Exception as e:
        traceback.print_exc()
        return await reply.edit("Ran into an error.")

@Client.on_message(filters.command(["upload","tgm"]))
async def uploadImages(_: Client,m:t.Message):
    try:
        reply = await m.reply_text("`Downloading...`")
        file = await getFile(m,15242880)
        if file is None:
            return await reply.edit("Reply to an image?")
        if file == 1:
            return await reply.edit("File size is too large")
        await reply.edit("`Uploading...`")
        imageURL = await upload(file)
        if imageURL is None:
            return await reply.edit("Ran into an error.")
        return await reply.edit(f"Image uploaded: {imageURL}",disable_web_page_preview=False)
    except Exception as e:
        traceback.print_exc()
        return await reply.edit("Ran into an error.")