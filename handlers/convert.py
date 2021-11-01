import logging
import os, os.path
import shutil, pathlib

from PIL import Image

from aiogram import types
from aiogram.dispatcher import FSMContext

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
    state = FSMContext(dp.storage, message.chat.id, message.chat.id)
    async with state.proxy() as data:
        data['curr_photos_count'] = 0


async def increase_photos_count(state: FSMContext):
    async with state.proxy() as data:
        data['curr_photos_count'] += 1


@dp.message_handler(state=ConvertImage.waiting_for_photos, content_types=['photo', 'text', 'document'])
async def process_photo_sending(message: types.Message, state: FSMContext):
    logging.info(f"User {message.chat.id} sending data.")

    if message.content_type == 'photo':
        await increase_photos_count(state)
        await process_download_photo(message, state)
    elif message.content_type == 'document':
        await process_download_document(message, state)
    elif message.content_type == 'text' and message.text == 'Конвертировать':
        await process_convert(message, state)
    elif message.content_type == 'text' and message.text == 'Отмена':
        await cancel_cmd(message, state)
        clear_memory(message)


def clear_memory(message: types.Message):
    shutil.rmtree(pathlib.Path('data', str(message.chat.id)))


async def cancel_cmd(message: types.Message, state: FSMContext):
    text = [
        "Процесс конвертирования отменён.",
        "Чтобы начать его заново введите команду /convert.",
    ]
    await message.answer('\n'.join(text), reply_markup=types.ReplyKeyboardRemove())
    await state.finish()


def jpg2pdf(message: types.Message):
    path_to_photos = pathlib.Path('data', str(message.chat.id), 'photos')
    name_of_files = os.listdir(path_to_photos)
    im1 = Image.open(fp=pathlib.Path(path_to_photos, str(name_of_files[0])))
    images = []
    for i in range(1, len(name_of_files)):
        images.append(Image.open(fp=pathlib.Path(path_to_photos, str(name_of_files[i]))).convert('RGB'))
    if len(images) != 0:
        im1.save(pathlib.Path('data', str(message.chat.id), 'result.pdf'),
                    save_all=True, append_images=images)
    else:
        im1.save(pathlib.Path('data', str(message.chat.id), 'result.pdf'))


async def process_convert(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if data['curr_photos_count'] == 0:
            await message.answer("Вы не отправили ни одной фотографии.")
            return
        else:
            await message.answer('Запускаю процесс конвертирования... Это займёт немного времени.',
                                 reply_markup=types.ReplyKeyboardRemove())
            jpg2pdf(message)
            path_to_pdf = pathlib.Path('data', str(message.chat.id), 'result.pdf')
            await message.answer_document(document=open(path_to_pdf, 'rb'), caption="Ваш PDF файл:)")
            clear_memory(message)
    await state.finish()


async def process_download_document(message: types.Message, state: FSMContext):
    pass


async def process_download_photo(message: types.Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(keyboard=buttons)
    async with state.proxy() as data:
        if data['curr_photos_count'] <= MAX_PHOTOS_COUNT:
            logging.info(f"Uploaded photo from user {message.chat.id}")
            photo = message.photo.pop()
            await photo.download(destination_dir=pathlib.Path('data', str(message.chat.id)))
        else:
            text = [
                "Отправлено максимальное количество фотографий.",
                "Нажмите кнопку 'Конвертировать'.",
            ]
            await message.answer('\n'.join(text), reply_markup=keyboard)
