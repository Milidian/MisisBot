# - *- coding: utf- 8 - *-

from aiogram import Router, Bot, F
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery

from tgbot.database.db_document import Documentx
from tgbot.database.db_users import UserModel
from tgbot.keyboards.inline_admin import (document_cancel_add_finl, document_cancel_edit_finl,
                                          delete_document_confirm_finl)
from tgbot.keyboards.inline_main import document_edit_finl
from tgbot.keyboards.inline_page import document_open_finl
from tgbot.utils.misc.bot_models import FSM, ARS
from tgbot.utils.misc_functions import convert_ask

router = Router(name=__name__)


############################## ИЗМЕНЕНИЕ ДОКУМЕНТА #############################
# Изменение текста документа
@router.callback_query(F.data.startswith("edit_text_document"))
async def admin_document_edit(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS, User: UserModel):
    document_id = int(call.data.split(":")[1])

    await state.set_state("here_edit_text_document")
    await state.update_data(here_document_id=document_id)

    await call.message.edit_text(
        "<b>✏️Введите новую информацию для документа</b>\n"
        "❕ Информация не должна превышать 4000 символов",
        reply_markup=document_cancel_edit_finl(document_id)
    )


# Принятие нового текста
@router.message(StateFilter("here_edit_text_document"))
async def admin_document_edit_get(message: Message, bot: Bot, state: FSM, arSession: ARS, User: UserModel):
    document_id = int((await state.get_data())['here_document_id'])

    if len(message.text) > 4000:
        return await message.answer(
            "<b>❌ Превышен лимит символов\n</b>"
            "❕ Информация документа не должна превышать 4000 символов",
            reply_markup=document_cancel_edit_finl(document_id)
        )

    document_file = None

    if message.document:
        document_file = message.document.file_id
    elif message.photo:
        document_file = message.photo[-1].file_id
    elif message.video:
        document_file = message.video.file_id
    else:
        document_file = message.text

    await state.clear()

    Documentx.update(
        document_id=document_id,
        document_info=document_file
    )

    get_document = Documentx.get(document_id=document_id)

    await message.answer(
        get_document.document_info,
        reply_markup=document_edit_finl(document_id, User.user_id, 0)
    )


# Изменение названия кнопки
@router.callback_query(F.data.startswith("edit_name_document:"))
async def admin_edit_name_document(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS, User: UserModel):
    document_id = int(call.data.split(":")[1])

    await state.set_state("here_edit_name_document")
    await state.update_data(here_document_id=document_id)

    await call.message.edit_text(
        "<b>✏️Введите новое название для документа</b>\n"
        "❕ Название не должно превышать 50 символов",
        reply_markup=document_cancel_edit_finl(document_id)
    )


# Принятие нового названия кнопки
@router.message(StateFilter("here_edit_name_document"))
async def admin_document_edit_name_get(message: Message, bot: Bot, state: FSM, arSession: ARS, User: UserModel):
    document_id = int((await state.get_data())['here_document_id'])

    if len(message.text) > 50:
        return message.answer(
            "<b>❌ Превышен лимит символов</b>\n"
            "❕ Длина документа не должна превышать 50 символов",
            reply_markup=document_cancel_edit_finl(document_id)
        )

    Documentx.update(
        document_id=document_id,
        document_name=message.text
    )

    get_document = Documentx.get(document_id=document_id)

    await message.answer(
        get_document.document_info,
        reply_markup=document_edit_finl(document_id, User.user_id, 0)
    )


############################## СОЗДАНИЕ ДОКУМЕНТА ##############################
# Создание названия документа
@router.callback_query(F.data == "document_add")
async def admin_document_name_add(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS, User: UserModel):
    await state.set_state("here_document_name_create")

    await call.message.edit_text(
        "<b>✏️ Введите название для документа\n</b>"
        "❕ Длина не должна превышать 50 символов",
        reply_markup=document_cancel_add_finl()
    )


# Создание информации в документе
@router.message(StateFilter("here_document_name_create"))
async def admin_document_info_add(message: Message, bot: Bot, state: FSM, arSession: ARS, User: UserModel):
    if len(message.text) > 50:
        return message.answer(
            "<b>❌ Превышен лимит символов</b>\n"
            "❕ Длина документа не должна превышать 50 символов",
            reply_markup=document_cancel_add_finl()
        )

    await state.update_data(here_document_name=message.text)
    await state.set_state("here_document_info_create")

    await message.answer(
        "<b>✏️ Введите информацию для документа\n</b>"
        "❕ Информация не должна превышать 4000 символов",
        reply_markup=document_cancel_add_finl()
    )


# Создание документа
@router.message(StateFilter("here_document_info_create"))
async def admin_document_info_add(message: Message, bot: Bot, state: FSM, arSession: ARS, User: UserModel):
    if len(message.text) > 4000:
        return message.answer(
            "<b>❌ Превышен лимит символов\n</b>"
            "❕ Информация документа не должна превышать 4000 символов",
            reply_markup=document_cancel_add_finl()
        )

    get_document_name = (await state.get_data())['here_document_name']
    get_document_info = message.text

    await state.clear()

    Documentx.add(
        document_name=get_document_name,
        document_info=get_document_info,
    )

    await message.answer(
        "<b>📔 Выберите документ для информации о нём</b>",
        reply_markup=document_open_finl(message.from_user.id, 0)
    )


# Отмена создания документа
@router.callback_query(F.data == "document_cancel_add")
async def admin_document_add(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS, User: UserModel):
    await state.clear()

    await call.message.edit_text(
        "<b>📔 Выберите документ для информации о нём</b>",
        reply_markup=document_open_finl(call.from_user.id, 0)
    )


############################## УДАЛЕНИЕ ДОКУМЕНТА ##############################
# Удаление документа
@router.callback_query(F.data.startswith("delete_document"))
async def admin_document_delete(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS, User: UserModel):
    document_id = int(call.data.split(":")[1])

    await call.message.edit_text(
        "❗️ Вы уверены что хотите удалить этот документ?",
        reply_markup=delete_document_confirm_finl(document_id)
    )


# Подтверждение удаления документа
@router.callback_query(F.data.startswith("delete_confirm"))
async def admin_document_delete(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS, User: UserModel):
    document_id = int(call.data.split(":")[1])

    Documentx.delete(document_id=document_id)

    await call.answer("✅ Документ успешно удалён")
    await call.message.edit_text(
        "<b>📔 Выберите документ для информации о нём</b>",
        reply_markup=document_open_finl(call.from_user.id, 0)
    )


################################## ПОДДЕРЖКА ###################################
# Ответ на вопрос в поддержку
@router.callback_query(F.data.startswith("support_admin_answer"))
async def admin_support_cancel(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS, User: UserModel):
    user_id = call.data.split(":")[1]  # Айди пользователя задавшего вопрос

    await state.set_state("here_support_ask")
    await state.update_data(here_user_id=user_id)

    await bot.delete_message(
        chat_id=User.user_id,
        message_id=call.message.message_id
    )

    await call.message.answer(
        "<b>📝 Введите ответ на вопрос</b>\n"
        "❕ Длина ответа не должна превышать 2000 символов",
    )


# Принятие ответа на вопрос
@router.message(StateFilter("here_support_ask"))
async def admin_support_ask(message: Message, bot: Bot, state: FSM, arSession: ARS, User: UserModel):
    if len(message.text) > 2000:
        return await message.answer(
            "<b>❌ Превышен лимит символов\n</b>"
            "❕ Ответ не должен превышать 2000 символов"
        )

    get_user_id = (await state.get_data())['here_user_id']

    await state.clear()

    await bot.delete_message(
        chat_id=User.user_id,
        message_id=message.message_id - 1
    )

    await bot.send_message(
        chat_id=get_user_id,
        text=convert_ask(message.text)
    )

    await message.answer("✅ Ответ успешно отправлен")
