# Copyright 2024 Qewertyy, MIT License

from aiogram import types, filters
from bot import dp
from utils import getText, ImageGeneration
from bot import Models
from config import Config

Database = {}


@dp.message_handler(
    filters.Command(
        commands=["dream", "create", "imagine", "draw"],
        prefixes="!/",
        ignore_case=False,
    )
)
async def draw(m: types.Message):
    global Database
    prompt = getText(m)
    if prompt is None:
        return await m.reply("give something to create")
    user = m.from_user
    data = {"prompt": prompt, "reply_to_id": m.message_id}
    Database[user.id] = data
    rows = []
    markup = types.InlineKeyboardMarkup()
    for index, model in enumerate(Models):
        button = types.InlineKeyboardButton(
            model["name"], callback_data=f"d.{model['id']}.{user.id}"
        )
        if index % 2 == 0:
            rows.append([button])
        else:
            rows[-1].append(button)
    markup = types.InlineKeyboardMarkup(row_width=2)
    for row in rows:
        markup.row(*row)
    markup.add(
        types.InlineKeyboardButton(
            "Cancel", callback_data=f"d.-1.{user.id}"
        ))
    await m.reply(
        text=f"Your prompt: `{prompt}`\n\nSelect a model",
        reply_markup=markup,
        parse_mode=types.ParseMode.MARKDOWN,
    )


@dp.callback_query_handler(filters.Regexp(r"d\.\d+\.\d+"))
async def selectModel(query: types.CallbackQuery):
    global Database
    data = query.data.split(".")
    auth_user = int(data[-1])
    if query.from_user.id != auth_user:
        return await query.answer("No.")
    modelId = int(data[1])
    if modelId == -1:
        del Database[auth_user]
        await query.message.delete()
        return
    await query.message.edit_text("Please wait, generating your image")
    promptData = Database.get(auth_user, None)
    if promptData is None:
        return await query.message.edit_text("Something went wrong.")
    img_url = await ImageGeneration(modelId, promptData["prompt"])
    print(img_url)
    if img_url is None or img_url == 2 or img_url == 1:
        return await query.message.edit_text("something went wrong!")
    elif img_url == 69:
        return await query.message.edit_text("NSFW not allowed!")
    images = []
    logimg = []
    modelName = [i["name"] for i in Models if i["id"] == modelId]
    for i in img_url:
        images.append(types.InputMediaDocument(i))
        logimg.append(types.InputMediaDocument(i))
    images[-1] = types.InputMediaDocument(
        img_url[-1],
        caption=f"Your Prompt: `{promptData['prompt']}`\nModel: `{modelName[0]}`",
        parse_mode=types.ParseMode.MARKDOWN,
    )  # for caption
    await query.message.delete()
    try:
        del Database[auth_user]
    except KeyError:
        pass
    await dp.bot.send_media_group(
        chat_id=query.message.chat.id,
        media=images,
        reply_to_message_id=promptData["reply_to_id"],
        parse_mode=types.ParseMode.MARKDOWN,
    )
