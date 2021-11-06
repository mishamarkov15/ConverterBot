import os
import pathlib
import shutil

from aiogram import Dispatcher, executor

from loader import dp
import handlers
import logging
from utils.set_bot_commands import set_default_commands


async def on_startup(dp: Dispatcher):
    logging.basicConfig(level=logging.INFO)
    pathlib.Path('data').mkdir(exist_ok=True)
    for id_val in os.listdir(pathlib.Path('data')):
        shutil.rmtree(pathlib.Path('data', id_val))
    await set_default_commands(dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
