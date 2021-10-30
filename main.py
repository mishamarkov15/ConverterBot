from aiogram import Dispatcher, executor

from misc import dp
import handlers
import logging
from utils.set_bot_commands import set_default_commands


async def on_startup(dp: Dispatcher):
    logging.basicConfig(level=logging.INFO)
    await set_default_commands(dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
