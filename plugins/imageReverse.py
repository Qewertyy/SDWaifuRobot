# Copyright 2023 Qewertyy, MIT License
import traceback
from pyrogram import Client, filters, types as t
from Utils import ReverseImageSearch, getFile, createMessage, upload


@Client.on_message(filters.command(["pp", "reverse", "sauce"]))
async def reverseImageSearch(_: Client, m: t.Message):
    try:
        reply = await m.reply_text("`Downloading...`")
        file = await getFile(m)
        if file is None:
            return await reply.edit("Reply to an image?")
        if file == 1:
            return await reply.edit("File size is large")
        await reply.edit("`Uploading to the server...`")
        imageURL = await upload(file)
        if imageURL is None:
            return await reply.edit("Ran into an error.")
        collId = f"ris-{m.from_user.id}"
        _.db[collId] = imageURL
        await reply.edit_text(
            text="Select a search engine",
            reply_markup=t.InlineKeyboardMarkup(
                [
                    [
                        t.InlineKeyboardButton(
                            text="Google",
                            callback_data=f"ris.g.{collId}.{m.from_user.id}",
                        )
                    ],
                    [
                        t.InlineKeyboardButton(
                            text="Bing",
                            callback_data=f"ris.b.{collId}.{m.from_user.id}",
                        )
                    ],
                    [
                        t.InlineKeyboardButton(
                            text="Yandex",
                            callback_data=f"ris.y.{collId}.{m.from_user.id}",
                        )
                    ],
                ]
            ),
        )
    except Exception as E:
        traceback.print_exc()
        await reply.delete()
        return await m.reply_text("Ran into an error.")


@Client.on_callback_query(filters.regex(r"^ris.(.*?)"))
async def ReverseResults(_: Client, query: t.CallbackQuery):
    data = query.data.split(".")
    userId = int(data[-1])
    collId = data[2]
    imageUrl = _.db.get(collId,None)
    if imageUrl is None:
        return await query.edit_message_text("Ran into an error.")
    platform = "bing" if data[1] == "b" else "google" if data[1] == "g" else "yandex"
    if query.from_user.id != userId:
        return await query.answer("Not for you!", show_alert=True)
    output = await ReverseImageSearch(imageUrl, platform)
    try:
        del _.db[collId]
    except KeyError:
        pass
    if output["code"] != 2:
        return await query.edit_message_text("Ran into an error.")
    messages = createMessage(platform, output["content"])
    btn = t.InlineKeyboardMarkup(
        [[t.InlineKeyboardButton(text="Image URL", url=output["content"]["url"])]]
    )
    await query.edit_message_text(messages["message"], reply_markup=btn)
