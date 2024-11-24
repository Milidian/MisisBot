# - *- coding: utf- 8 - *-
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tgbot.utils.const_functions import ikb


################################## ПОДДЕРЖКА ###################################
# Отмена поддержки
def support_cancel_finl() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("Отменить", data=f"support_cancel"),
    )

    return keyboard.as_markup()