# - *- coding: utf- 8 - *-
from aiogram import Bot
from aiogram.types import FSInputFile

from tgbot.data.config import get_admins, PATH_DATABASE, BOT_STATUS_NOTIFICATION
from tgbot.database.db_users import Userx
from tgbot.utils.const_functions import get_date, send_admins, ded, convert_date, get_unix


# Вопрос для администрации
def convert_question(text: str, user_id: int):
    get_user = Userx.get(user_id=user_id)

    return ded(f"""
        {text}
        
        ➖➖➖➖➖➖➖➖➖➖
        <b>👤 Вопрос от: <b>@{get_user.user_login}</b>
        ⌛️ Время отправления вопроса: <code>{convert_date(get_unix())}</code></b>
    """)


# Ответ для пользователя
def convert_ask(text: str):
    return ded(f"""
        <b>Ответ от администратора</b>
        ➖➖➖➖➖➖➖➖➖➖
    
        {text}
    """)


# Выполнение функции после запуска бота (рассылка админам о запуске бота)
async def startup_notify(bot: Bot):
    if len(get_admins()) >= 1 and BOT_STATUS_NOTIFICATION:
        await send_admins(bot, "<b>✅ Бот был успешно запущен</b>")


# Автоматические бэкапы БД
async def autobackup_admin(bot: Bot):
    for admin in get_admins():
        try:
            await bot.send_document(
                admin,
                FSInputFile(PATH_DATABASE),
                caption=f"<b>📦 #AUTOBACKUP | <code>{get_date()}</code></b>",
            )
        except:
            ...
