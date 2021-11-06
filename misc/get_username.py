from aiogram import types


def define_username(message: types.Message):
    return message.chat.first_name if message.chat.first_name else message.chat.username
