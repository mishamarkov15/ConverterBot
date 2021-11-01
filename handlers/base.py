import logging

from aiogram import types
from aiogram.dispatcher.filters import CommandHelp, CommandStart
from aiogram.utils import markdown

from misc import bot, dp, emoji, define_username


@dp.message_handler(CommandStart())
async def cmd_start(message: types.Message):
    logging.info(f"User {message.chat.id} requested {message.text}")
    text = [
        f"Привет, {define_username(message)}! {emoji['waving hand sign']}\n",
        f"Я умею {markdown.hbold('конфертировать изображения в PDF')} файл.",
        "Доступные форматы изображений: jpg, jpeg, png.",
    ]
    await message.answer("\n".join(text), reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(CommandHelp())
async def cmd_help(message: types.Message):
    logging.info(f"User {message.chat.id} requested {message.text}.")
    text = [
        f"{markdown.hbold('Здесь список того, что я умею делать.')}\n",
        "/start - Начать работу со мной.",
        "/help - Получить это сообщение.",
        "/convert - Начать процесс конвертации.",
    ]
    await message.answer("\n".join(text))
