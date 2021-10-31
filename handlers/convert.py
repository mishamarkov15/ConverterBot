import logging
import os, os.path
import shutil

from PIL import Image

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from config import MAX_PHOTOS_COUNT
from misc import dp
from states.convert_image import ConvertImage


buttons = [
        [types.KeyboardButton(text='Конвертировать', )],
        [types.KeyboardButton(text='Отмена')],
    ]


@dp.message_handler(commands=['convert'])
async def cmd_convert(message: types.Message):
    logging.info(f"User {message.chat.id} requested {message.text}")
    text = [
        "Отправьте мне фото.",
        f"Всего можно отправить до {MAX_PHOTOS_COUNT} фото.",
    ]
    keyboard = types.ReplyKeyboardMarkup(buttons)
    await message.answer('\n'.join(text), reply_markup=keyboard)
    await ConvertImage.waiting_for_photos.set()


def clear_memory():
    shutil.rmtree('/home/mikhail/PycharmProjects/Bot_test/data/986374492')


async def cancel_cmd(message: types.Message, state: FSMContext):
    text = [
        "Процесс конвертирования отменён.",
        "Чтобы начать его заново введите команду /convert.",
    ]
    await message.answer('\n'.join(text), reply_markup=types.ReplyKeyboardRemove())
    await state.finish()


async def jpg2pdf(message: types.Message):
    path_to_photos = '/home/mikhail/PycharmProjects/Bot_test/data/' + str(message.chat.id) + '/photos'
    name_of_files = os.listdir(path_to_photos)
    im1 = Image.open(path_to_photos + '/' + str(name_of_files[0])).convert('RGB')
    images = []
    for i in range(1, len(name_of_files)):
        images.append(Image.open(path_to_photos + '/' + str(name_of_files[i])).convert('RGB'))
    if len(images) != 0:
        im1.save('/home/mikhail/PycharmProjects/Bot_test/data/' + str(message.chat.id) + '/result.pdf',
                    save_all=True, append_images=images)
    else:
        im1.save('/home/mikhail/PycharmProjects/Bot_test/data/' + str(message.chat.id) + '/result.pdf')


async def process_convert(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if data['curr_photos_count'] == 0:
            await message.answer("Вы не отправили ни одной фотографии.")
            return
        else:
            await message.answer('Запускаю процесс конвертирования... Это займёт немного времени.',
                                 reply_markup=types.ReplyKeyboardRemove())
            await jpg2pdf(message)
    await state.finish()


async def process_download_photo(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(keyboard=buttons)
    async with state.proxy() as data:
        if data['curr_photos_count'] < MAX_PHOTOS_COUNT:
            photo = message.photo.pop()
            await photo.download(destination_dir='/home/mikhail/PycharmProjects/Bot_test/data/' + str(message.chat.id))
            data['curr_photos_count'] += 1
            await message.answer(f"Фото добавлено. Ещё можно добавить {MAX_PHOTOS_COUNT - data['curr_photos_count']}.")
        else:
            text = [
                "Отправлено максимальное количество фотографий.",
                "Нажмите кнопку 'Конвертировать'.",
            ]
            await message.answer('\n'.join(text), reply_markup=keyboard)


@dp.message_handler(state=ConvertImage.waiting_for_photos, content_types=['photo', 'text', 'document'])
async def process_photo_sending(message: types.Message, state: FSMContext):
    logging.info(f"User {message.chat.id} sending data.")

    async with state.proxy() as data:
        if 'curr_photos_count' not in data.keys():
            data['curr_photos_count'] = 0

    if message.content_type == 'photo' or message.content_type == 'document':
        await process_download_photo(message, state)
    elif message.content_type == 'text' and message.text == 'Конвертировать':
        await process_convert(message, state)
        await message.answer_document()
    elif message.content_type == 'text' and message.text == 'Отмена':
        await cancel_cmd(message, state)
        clear_memory()
    print(message.content_type)
