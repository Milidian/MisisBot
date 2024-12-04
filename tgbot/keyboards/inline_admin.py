# - *- coding: utf- 8 - *-
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from tgbot.utils.const_functions import ikb


########################### РЕДАКТИРОВАНИЕ ДОКУМЕНТА ###########################
# Отмена редактирования
def document_edit_cancel_finl(document_id: int)  -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("Отменить", data=f"document_open:{document_id}:{0}"),
    )

    return keyboard.as_markup()


# Подтверждение удаления документа
def document_edit_delete_confirm_finl(document_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("Подтвердить", data=f"document_delete_confirm:{document_id}"),
        ikb("🔙 Назад", data=f"document_open:{document_id}:0")
    )

    return keyboard.as_markup()


############################## СОЗДАНИЕ ДОКУМЕНТА ##############################
# Отмена создания документа
def document_cancel_add_finl() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("Отменить", data=f"document_cancel_add"),
    )

    return keyboard.as_markup()


################################## ПОДДЕРЖКА ###################################
# Отмена поддержки
def support_cancel_finl() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("Отменить", data=f"support_cancel"),
    )

    return keyboard.as_markup()


# Ответ на вопрос в поддержку
def support_admin_answer_finl(user_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.row(
        ikb("✏️ Ответить", data=f"support_admin_answer:{user_id}"),
    )

    return keyboard.as_markup()
