# Copyright 2023 Qewertyy, MIT License

from pyrogram import Client, filters, types as t,errors
from Utils import getText,SearchImages,getImageContent
import traceback,random,datetime,os

@Client.on_message(filters.command(["img","image","imagesearch"]))
async def searchImages(_: Client,m:t.Message):
    try:
        reply = await m.reply_text("`Searching...`")
        prompt = getText(m)
        if prompt is None:
            return await reply.edit("What do you want to search?")
        output = await SearchImages(prompt,"google")
        if output['code'] != 2:
            await reply.delete()
            return await reply.edit("Ran into an error.")
        images = random.choices(output['content'],k=8)
        if len(images) == 0:
            await reply.delete()
            return await reply.edit("No results found.")
        media = []
        filePaths = []
        for image in images:
            print(image['imageUrl'])
            content,imageType = getImageContent(image['imageUrl'])
            if content is None:
                images.remove(image)
                continue
            else:
                path = f"./downloads/{m.from_user.id}_{datetime.datetime.now().timestamp()}.{imageType}"
                with open(path, "wb") as f:
                    f.write(content)
                filePaths.append(path)
                media.append(t.InputMediaPhoto(path))
        await _.send_media_group(
            m.chat.id,
            media,
            reply_to_message_id=m.id
            )
        await reply.delete()
        for image in filePaths:
            if os.path.exists(image):
                os.remove(image)
    except (errors.ExternalUrlInvalid, errors.WebpageCurlFailed,errors.WebpageMediaEmpty) as e:
        print(e)
        await reply.delete()
        return await reply.edit("Ran into an error.")
    except Exception as e:
        traceback.print_exc()
        await reply.delete()
        return await m.reply_text("Ran into an error.")