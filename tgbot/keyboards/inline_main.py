# - *- coding: utf- 8 - *-
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tgbot.data.config import get_admins
from tgbot.utils.const_functions import ikb


################################## ДОКУМЕНТЫ ###################################
# Кнопки действий с документом
def document_edit_finl(document_id: int, user_id: int, remover: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    if user_id in get_admins():
        keyboard.row(
            ikb("🛠 Изм. текст", data=f"edit_text_document:{document_id}"),
            ikb("🛠 Изм. название", data=f"edit_name_document:{document_id}")
        ).row(
            ikb("🗑 Удалить", data=f"delete_document:{document_id}"),
        )

    keyboard.row(
        ikb("🔙 Назад", data=f"open_document:{document_id}")
    )

    return keyboard.as_markup()
