from config import BOT_COMMANDS
from aiogram import Dispatcher


async def set_default_commands(dp: Dispatcher):
    await dp.bot.set_my_commands(BOT_COMMANDS)
