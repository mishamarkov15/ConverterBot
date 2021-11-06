import logging

from aiogram import types

from loader import dp
from texts.support_text import get_support_text
from keyboards.support_handler import support_references


@dp.callback_query_handler(lambda c: c.data == 'mail')
async def send_telegram_ref(call: types.CallbackQuery):
    await call.message.answer(text='misha.markov-03@mail.ru')


@dp.message_handler(commands=['support'])
async def cmd_support(message: types.Message):
    logging.info(f"User {message.chat.id} requested support")
    text = get_support_text()
    await message.answer(text=''.join(text), reply_markup=support_references)
