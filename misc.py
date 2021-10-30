from aiogram import Bot, Dispatcher, types

import config

emoji = {
    'waving hand sign': '\U0001F44B',
}

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


def define_username(message: types.Message):
    return message.chat.first_name if message.chat.first_name else message.chat.username
