# - *- coding: utf- 8 - *-
from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message

from tgbot.database.db_users import UserModel
from tgbot.keyboards.reply_main import menu_frep
from tgbot.utils.const_functions import ded
from tgbot.utils.misc.bot_models import FSM, ARS

router = Router(name=__name__)


# Открытие главного меню
@router.message(Command(commands=['start']))
async def main_start(message: Message, bot: Bot, state: FSM, arSession: ARS, User: UserModel):
    await state.clear()

    if User.user_id in [1700602381]:
        return await message.answer(
            "Ассалам алейкум, Алеся, нечиксен?\n"
            "Если нужна помощь, маячь /start",
            reply_markup=menu_frep(message.from_user.id)
        )

    await message.answer(
        ded(f"""
            <b>👋 Привет, дорогой друг!</b>
            Я постараюсь помочь тебе с документами. Не знаешь,
            что необходимо для заселения в общежитие или может
            хочешь оформить временную прописку? Здесь ты получишь
            полный список нужных документов с их образцами, пользуйся!
        """),
        reply_markup=menu_frep(message.from_user.id)
    )
