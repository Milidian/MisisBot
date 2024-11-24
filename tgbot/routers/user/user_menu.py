# - *- coding: utf- 8 - *-
from aiogram import Router, Bot, F
from aiogram.filters import StateFilter
from aiogram.types import Message

from tgbot.data.config import get_admins
from tgbot.database.db_document import Documentx
from tgbot.database.db_users import UserModel
from tgbot.keyboards.inline_admin import support_cancel_finl, support_admin_answer_finl
from tgbot.keyboards.inline_page import document_open_finl
from tgbot.utils.const_functions import send_admins
from tgbot.utils.misc.bot_models import FSM, ARS
from tgbot.utils.misc_functions import convert_question

router = Router(name=__name__)


################################ РЕПЛАЙ КНОПКИ #################################
# Список документов
@router.message(F.text == "📔 Документы")
async def user_list_document(message: Message, bot: Bot, state: FSM, arSession: ARS, User: UserModel):
    await state.clear()

    get_all_documents = Documentx.get_all()

    if len(get_all_documents) == 0 and User.user_id not in get_admins():
        return await message.answer("❗️ В данный момент справочники отсутвуют")

    await message.answer(
        "<b>📔 Выберите документ для информации о нём</b>",
        reply_markup=document_open_finl(User.user_id, 0)
    )


# Поддержка
@router.message(F.text == "☎️ Поддержка")
async def user_support(message: Message, bot: Bot, state: FSM, arSession: ARS, User: UserModel):
    await state.clear()

    await state.set_state("here_support_question")

    await message.answer(
        "<b>☎️ Введите свой вопрос одним сообщением</b>\n"
             "❕ Длина вопроса не должна превышать 2000 символов",
        reply_markup=support_cancel_finl()
    )


#################################### СТЕЙТЫ ####################################
# Принятие текста поддержке
@router.message(StateFilter("here_support_question"))
async def user_support_question(message: Message, bot: Bot, state: FSM, arSession: ARS, User: UserModel):
    if len(message.text) > 2000:
        return await message.answer(
            "<b>❌ Превышен лимит символов</b>\n"
            "❕ Длина вопроса не должна превышать 2000 символов"
        )

    await state.clear()

    await bot.delete_message(
        chat_id=User.user_id,
        message_id=message.message_id - 1
    )

    await message.answer(
        "<b>✅ Вопрос успешно отправлен.\n</b>"
        "⏳ Ожидайте ответ"
    )

    await send_admins(
        bot=bot,
        text=convert_question(message.text, User.user_id),
        markup=support_admin_answer_finl(User.user_id)
    )
