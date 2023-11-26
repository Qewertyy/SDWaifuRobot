# Copyright 2023 Qewertyy, MIT License

from pyrogram.types import InlineKeyboardButton
from math import ceil

class EqInlineKeyboardButton(InlineKeyboardButton):
    def __eq__(self, other):
        return self.text == other.text

    def __lt__(self, other):
        return self.text < other.text

    def __gt__(self, other):
        return self.text > other.text

def paginate_models(page_n: int, models: list,user_id) -> list:
    modules = sorted(
        [
            EqInlineKeyboardButton(
            x['name'],
            callback_data=f"d.{x['id']}.{user_id}"
                )
                for x in models
            ]
            )

    pairs = list(zip(modules[::2], modules[1::2]))
    i = 0
    for m in pairs:
        for _ in m:
            i += 1
    if len(modules) - i == 1:
        pairs.append((modules[-1],))
    elif len(modules) - i == 2:
        pairs.append(
            (
                modules[-2],
                modules[-1],
            )
        )

    COLUMN_SIZE = 3

    max_num_pages = ceil(len(pairs) / COLUMN_SIZE)
    modulo_page = page_n % max_num_pages

    # can only have a certain amount of buttons side by side
    if len(pairs) > COLUMN_SIZE:
        pairs = pairs[
            modulo_page * COLUMN_SIZE : COLUMN_SIZE * (modulo_page + 1)
        ] + [
            (
                EqInlineKeyboardButton(
                    "⬅️",
                    callback_data=f"d.left.{modulo_page}.{user_id}"
                ),
                EqInlineKeyboardButton(
                    "Cancel",
                    callback_data=f"d.-1.{user_id}"
                ),
                EqInlineKeyboardButton(
                    "➡️",
                    callback_data=f"d.right.{modulo_page}.{user_id}"
                ),
            )
        ]
    else:
        pairs += [[EqInlineKeyboardButton("Cancel", callback_data=f"d.-1.{user_id}")]]

    return pairs
