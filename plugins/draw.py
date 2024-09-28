# Copyright 2023 Qewertyy, MIT License

from pyrogram import Client, filters, types as t
from Utils import getText,paginate_models,ImageGeneration

@Client.on_message(filters.command(["draw","create","imagine","dream"]))
async def draw(_: Client, m: t.Message):
    prompt = getText(m)
    if prompt is None:
        return await m.reply_text("give something to create")
    user = m.from_user
    data = {'prompt':prompt,'reply_to_id':m.id}
    _.db[f"draw-{user.id}"]= data
    btns = paginate_models(0,_.models,user.id)
    await m.reply_text(
            text=f"Your prompt: `{prompt}`\n\nSelect a model",
            reply_markup=t.InlineKeyboardMarkup(btns)
            )

@Client.on_callback_query(filters.regex(pattern=r"^d.(.*)"))
async def selectModel(_:Client,query:t.CallbackQuery):
    data = query.data.split('.')
    auth_user = int(data[-1])
    collectionId = f"draw-{auth_user}"
    if query.from_user.id != auth_user:
        return await query.answer("No.")
    if len(data) > 3:
        if data[1] == "right":
            next_page = int(data[2])
            await query.edit_message_reply_markup(
                t.InlineKeyboardMarkup(
                    paginate_models(next_page + 1,_.models,auth_user)
                    )
                )
        elif data[1] == "left":
            curr_page = int(data[2])
            await query.edit_message_reply_markup(
                t.InlineKeyboardMarkup(
                    paginate_models(curr_page - 1,_.models,auth_user)
                )
            )
        return
    modelId = int(data[1])
    if modelId == -1:
        del _.db[collectionId]
        await query.message.delete()
        return
    await query.edit_message_text("Please wait, generating your image")
    promptData = _.db.get(collectionId,None)
    if promptData is None:
        return await query.edit_message_text("Something went wrong.")
    img_url = await ImageGeneration(modelId,promptData['prompt'])
    if img_url is None or img_url == 2 or img_url ==1:
        return await query.edit_message_text("something went wrong!")
    elif img_url == 69:
        return await query.edit_message_text("NSFW not allowed!")
    images = []
    modelName = [i['name'] for i in _.models if i['id'] == modelId]
    for i in img_url:
        images.append(t.InputMediaDocument(i))
    images[-1] = t.InputMediaDocument(img_url[-1],caption=f"Your prompt: `{promptData['prompt']}`\nModel: `{modelName[0]}`") # for caption
    await query.message.delete()
    try:
        del _.db[collectionId]
    except KeyError:
        pass
    await _.send_media_group(
        chat_id=query.message.chat.id,
        media=images,
        reply_to_message_id=promptData['reply_to_id']
    )