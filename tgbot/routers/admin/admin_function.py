# - *- coding: utf- 8 - *-
from aiogram import Router, Bot, F
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery, ReactionTypeEmoji

from tgbot.database.db_document import Documentx
from tgbot.database.db_users import UserModel
from tgbot.keyboards.inline_admin import (document_cancel_add_finl, document_edit_cancel_finl,
                                          document_edit_delete_confirm_finl)
from tgbot.keyboards.inline_main import document_edit_finl
from tgbot.keyboards.inline_page import document_open_finl
from tgbot.utils.const_functions import del_message
from tgbot.utils.misc.bot_models import FSM, ARS
from tgbot.utils.misc_functions import convert_text_ask

router = Router(name=__name__)


############################## ИЗМЕНЕНИЕ ДОКУМЕНТА #############################
# Изменение текста документа
@router.callback_query(F.data.startswith("document_edit_text:"))
async def admin_document_edit(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS, User: UserModel):
    document_id = int(call.data.split(":")[1])

    await state.set_state("here_document_edit_text")
    await state.update_data(here_document_id=document_id)

    await call.message.edit_text(
        "<b>✏️Введите новую информацию для документа</b>\n"
        "❕ Информация не должна превышать 4000 символов",
        reply_markup=document_edit_cancel_finl(document_id)
    )


# Принятие нового текста
@router.message(StateFilter("here_document_edit_text"))
async def admin_document_edit_get(message: Message, bot: Bot, state: FSM, arSession: ARS, User: UserModel):
    document_id = (await state.get_data())['here_document_id']

    if len(message.text) > 4000:
        return await message.answer(
            "<b>❌ Превышен лимит символов\n</b>"
            "❕ Информация документа не должна превышать 4000 символов",
            reply_markup=document_edit_cancel_finl(document_id)
        )

    await state.clear()

    Documentx.update(
        document_id=document_id,
        document_info=message.text
    )

    get_document = Documentx.get(document_id=document_id)

    await message.answer(
        get_document.document_info,
        reply_markup=document_edit_finl(document_id, User.user_id, 0)
    )


# Изменение названия кнопки
@router.callback_query(F.data.startswith("document_edit_name:"))
async def admin_document_edit_name(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS, User: UserModel):
    document_id = int(call.data.split(":")[1])

    await state.set_state("here_document_edit_name")
    await state.update_data(here_document_id=document_id)

    await call.message.edit_text(
        "<b>✏️ Введите новое название для документа</b>\n"
        "❕ Название не должно превышать 50 символов",
        reply_markup=document_edit_cancel_finl(document_id)
    )


# Принятие нового названия кнопки
@router.message(StateFilter("here_document_edit_name"))
async def admin_document_edit_name_get(message: Message, bot: Bot, state: FSM, arSession: ARS, User: UserModel):
    document_id = int((await state.get_data())['here_document_id'])

    if len(message.text) > 50:
        return message.answer(
            "<b>❌ Превышен лимит символов</b>\n"
            "❕ Длина документа не должна превышать 50 символов",
            reply_markup=document_edit_cancel_finl(document_id)
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


# Удаление документа
@router.callback_query(F.data.startswith("document_edit_delete:"))
async def admin_document_delete(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS, User: UserModel):
    document_id = int(call.data.split(":")[1])

    await call.message.edit_text(
        "❗️ Вы уверены что хотите удалить этот документ?",
        reply_markup=document_edit_delete_confirm_finl(document_id)
    )


# Подтверждение удаления документа
@router.callback_query(F.data.startswith("document_delete_confirm"))
async def admin_document_delete_confirm(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS, User: UserModel):
    document_id = int(call.data.split(":")[1])

    Documentx.delete(document_id=document_id)

    await call.answer("<b>✅ Документ успешно удалён</b>")
    await call.message.edit_text(
        "<b>📔 Выберите документ для информации о нём</b>",
        reply_markup=document_open_finl(call.from_user.id, 0)
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


################################## ПОДДЕРЖКА ###################################
# Ответ на вопрос в поддержку
@router.callback_query(F.data.startswith("support_admin_answer"))
async def admin_support_cancel(call: CallbackQuery, bot: Bot, state: FSM, arSession: ARS, User: UserModel):
    user_id = call.data.split(":")[1]  # Айди пользователя задавшего вопрос

    await state.set_state("here_support_ask")
    await state.update_data(here_user_id=user_id)

    cache_message = await call.message.answer(
        "<b>📝 Введите ответ на вопрос</b>\n"
        "❕ Длина ответа не должна превышать 2000 символов",
    )
    await call.answer()

    await state.update_data(here_cache_message=cache_message)


# Принятие ответа на вопрос
@router.message(StateFilter("here_support_ask"))
async def admin_support_ask(message: Message, bot: Bot, state: FSM, arSession: ARS, User: UserModel):
    if len(message.text) > 2000:
        return await message.answer(
            "<b>❌ Превышен лимит символов\n</b>"
            "❕ Ответ не должен превышать 2000 символов"
        )

    user_id = (await state.get_data())['here_user_id']

    try:
        cache_message: Message = (await state.get_data())['here_cache_message']
    except:
        ...
    else:
        await del_message(cache_message)

    await bot.send_message(
        chat_id=user_id,
        text=convert_text_ask(message.text)
    )

    await message.react(reaction=[ReactionTypeEmoji(emoji="👌")])
    await state.clear()
