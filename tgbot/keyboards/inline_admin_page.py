# - *- coding: utf- 8 - *-
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tgbot.database.db_document import Documentx
from tgbot.keyboards.inline_helper import build_pagination_finl
from tgbot.utils.const_functions import ikb


############################## ИЗМЕНЕНИЕ ДОКУМЕНТА #############################
# Список документов для редактирования
def document_edit_page_finl(remover: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    get_documents = Documentx.get_all()

    for count, select in enumerate(range(remover, len(get_documents))):
        if count < 10:
            document = get_documents[select]

            keyboard.row(
                ikb(
                    document.document_name,
                    data=f"document_edit_open:{document.document_id}:{remover}",
                )
            )

    buildp_kb = build_pagination_finl(get_documents, f"document_edit_swipe", remover)
    keyboard.row(*buildp_kb)

    return keyboard.as_markup()
