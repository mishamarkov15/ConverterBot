import logging

from aiogram.dispatcher.filters import CommandHelp, CommandStart

from loader import dp
from texts.base_text import *
from misc.get_username import *


@dp.message_handler(CommandStart())
async def cmd_start(message: types.Message):
    logging.info(f"User {message.chat.id} requested {message.text}")
    text = start_text(message)
    await message.answer("".join(text), reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(CommandHelp())
async def cmd_help(message: types.Message):
    logging.info(f"User {message.chat.id} requested {message.text}.")
    text = help_text(message)
    await message.answer("".join(text))
