# - *- coding: utf- 8 - *-
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tgbot.data.config import get_admins
from tgbot.database.db_document import Documentx
from tgbot.keyboards.inline_helper import build_pagination_finl
from tgbot.utils.const_functions import ikb


############################## ОТКРЫТИЕ ДОКУМЕНТА ##############################
# Список документов
def document_open_finl(user_id: int, remover: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    get_documents = Documentx.get_all()

    for count, select in enumerate(range(remover, len(get_documents))):
        if count < 10:
            document = get_documents[select]

            keyboard.row(
                ikb(
                    document.document_name,
                    data=f"document_open:{document.document_id}:{remover}",
                )
            )

    buildp_kb = build_pagination_finl(get_documents, f"document_swipe", remover)
    keyboard.row(*buildp_kb)

    if user_id in get_admins():
        keyboard.row(
            ikb("➕ Добавить документ", data="document_add")
        )

    return keyboard.as_markup()