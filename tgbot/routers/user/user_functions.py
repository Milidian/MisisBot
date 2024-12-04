# - *- coding: utf- 8 - *-
from aiogram import Router, Bot, F
from aiogram.types import CallbackQuery

from tgbot.data.config import get_admins
from tgbot.database.db_document import Documentx
from tgbot.database.db_users import UserModel
from tgbot.keyboards.inline_main import document_edit_finl
from tgbot.keyboards.inline_page import document_open_finl
from tgbot.utils.misc.bot_models import FSM, ARS

router = Router(name=__name__)


############################## ДОКУМЕНТЫ ##############################
# Список документов
@router.callback_query(F.data.startswith("document_list:"))
async def user_document_list(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS, User: UserModel):
    remover = int(call.data.split(":")[1])

    get_all_documents = Documentx.get_all()

    if len(get_all_documents) == 0 and User.user_id not in get_admins():
        return await call.message.answer("❗️ В данный момент документы отсутвуют")

    await call.message.edit_text(
        "<b>📔 Выберите документ для информации о нём</b>",
        reply_markup=document_open_finl(User.user_id, 0)
    )


# Открытие документа
@router.callback_query(F.data.startswith("document_open:"))
async def user_document_open(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS, User: UserModel):
    document_id = int(call.data.split(":")[1])
    remover = int(call.data.split(":")[2])

    get_document = Documentx.get(document_id=document_id)

    await call.message.edit_text(
        get_document.document_info,
        reply_markup=document_edit_finl(document_id, User.user_id, remover)
    )


# Открытие докуента
@router.callback_query(F.data.startswith("document_swipe:"))
async def user_document_swipe(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS, User: UserModel):
    remover = int(call.data.split(":")[1])

    await call.message.edit_text(
        "<b>📔 Выберите документ для информации о нём</b>",
        reply_markup=document_open_finl(User.user_id, remover)
    )


################################## ПОДДЕРЖКА ###################################
# Отмена поддержки
@router.callback_query(F.data == "support_cancel")
async def user_support_cancel(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS, User: UserModel):
    await state.clear()

    await call.message.edit_text("<b>❕ Отмена поддержки</b>")
