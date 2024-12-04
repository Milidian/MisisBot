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


# Получение Базы Данных
@router.message(Command(commands=['db', 'database']))
async def admin_database(message: Message, bot: Bot, state: FSM, arSession: ARS, User: UserModel):
    await state.clear()

    await message.answer_document(
        FSInputFile(PATH_DATABASE),
        caption=f"<b>📦 #BACKUP | <code>{get_date()}</code></b>",
    )


# Получение логов
@router.message(Command(commands=['log', 'logs']))
async def admin_log(message: Message, bot: Bot, state: FSM, arSession: ARS, User: UserModel):
    await state.clear()

    media_group = MediaGroupBuilder(
        caption=f"<b>🖨 #LOGS | <code>{get_date(full=False)}</code></b>",
    )

    if os.path.isfile(PATH_LOGS):
        media_group.add_document(media=FSInputFile(PATH_LOGS))

    if os.path.isfile("tgbot/data/sv_log_err.log"):
        media_group.add_document(media=FSInputFile("tgbot/data/sv_log_err.log"))

    if os.path.isfile("tgbot/data/sv_log_out.log"):
        media_group.add_document(media=FSInputFile("tgbot/data/sv_log_out.log"))

    await message.answer_media_group(media=media_group.build())


# Очистить логи
@router.message(Command(commands=['clear_log', 'clear_logs', 'log_clear', 'logs_clear']))
async def admin_logs_clear(message: Message, bot: Bot, state: FSM, arSession: ARS, User: UserModel):
    await state.clear()

    if os.path.isfile(PATH_LOGS):
        async with aiofiles.open(PATH_LOGS, "w") as file:
            await file.write(f"{get_date()} | LOGS WAS CLEAR")

    if os.path.isfile("tgbot/data/sv_log_err.log"):
        async with aiofiles.open("tgbot/data/sv_log_err.log", "w") as file:
            await file.write(f"{get_date()} | LOGS WAS CLEAR")

    if os.path.isfile("tgbot/data/sv_log_out.log"):
        async with aiofiles.open("tgbot/data/sv_log_out.log", "w") as file:
            await file.write(f"{get_date()} | LOGS WAS CLEAR")

    await message.answer("<b>🖨 The logs have been cleared</b>")
