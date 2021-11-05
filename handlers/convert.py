import json
import logging
import os
import pathlib
import requests
import pyheif

from PIL import Image

from aiogram import types
from aiogram.dispatcher import FSMContext

from config import BOT_TOKEN, AVALIABLE_TYPES_FOR_PHOTO, emoji
from loader import dp
from states.convert_image import ConvertImage
from keyboards.convert_handler import *
from helpers.convert_helpers import create_folder, increase_photos_count, clear_memory
from texts.convert_image_text import *


@dp.message_handler(commands=['convert'])
async def cmd_convert(message: types.Message):
    logging.info(f"User {message.chat.id} requested {message.text}")
    create_folder(pathlib.Path('data'), f"{message.chat.id}")
    create_folder(pathlib.Path('data', f"{message.chat.id}"), 'photos')
    create_folder(pathlib.Path('data', f"{message.chat.id}"), 'documents')

    text = command_convert_image_text()
    await message.answer('\n'.join(text), reply_markup=keyboard_sending_photo_state)
    await ConvertImage.waiting_for_photos.set()

    state = FSMContext(dp.storage, message.chat.id, message.chat.id)
    async with state.proxy() as data:
        data['curr_photos_count'] = 0


async def cancel_cmd(message: types.Message, state: FSMContext):
    text = cancel_convert_image_text()
    await message.answer('\n'.join(text), reply_markup=types.ReplyKeyboardRemove())
    await state.finish()


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


def images_to_pdf_file(message: types.Message):
    images = []

    if pathlib.Path('data', str(message.chat.id), 'photos').exists():
        path_to_photos = pathlib.Path('data', str(message.chat.id), 'photos')
        for file in os.listdir(path_to_photos):
            images.append(Image.open(pathlib.Path(path_to_photos, str(file))).convert('RGB'))
        logging.info(f"All photos added to query successfully")

    if pathlib.Path('data', str(message.chat.id), 'documents').exists():
        path_to_photos = pathlib.Path('data', str(message.chat.id), 'documents')
        for file in os.listdir(path_to_photos):
            if file.split(sep='.')[1] in ['heic', 'heif', 'heic-sequence', 'heif-sequence']:
                bytes_data = pyheif.read(pathlib.Path(path_to_photos, str(file)))
                images.append(Image.frombytes(bytes_data.mode, bytes_data.size, bytes_data.data, 'raw',
                                              bytes_data.mode, bytes_data.stride))
            else:
                images.append(Image.open(pathlib.Path(path_to_photos, str(file))).convert('RGB'))

        logging.info(f"All image files added to query successfully")

    im1 = images[0]
    if len(images) != 0:
        im1.save(pathlib.Path('data', str(message.chat.id), 'result.pdf'),
                 save_all=True, append_images=images[1:])
    else:
        im1.save(pathlib.Path('data', str(message.chat.id), 'result.pdf'))
    logging.info(f"All images files and photos converted successfully")


async def process_convert(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if data['curr_photos_count'] == 0:
            await message.answer("Вы не отправили ни одной фотографии.")
            return
        else:
            logging.info(f"Converting process started")
            await message.answer('Запускаю процесс конвертирования... Это займёт не более 5 минут.',
                                 reply_markup=types.ReplyKeyboardRemove())

            images_to_pdf_file(message)
            path_to_pdf = pathlib.Path('data', str(message.chat.id), 'result.pdf')
            await message.answer_document(document=open(path_to_pdf, 'rb'),
                                          caption=f"Ваш PDF файл. Спасибо,  что доверили мне эту работу "
                                                  f"{emoji['smiling_face']}")
            clear_memory(message)
    await state.finish()


async def process_download_document(message: types.Message, state: FSMContext):
    if message.document.mime_type in AVALIABLE_TYPES_FOR_PHOTO:
        await increase_photos_count(state)
        async with state.proxy() as data:
            if data['curr_photos_count'] <= MAX_PHOTOS_COUNT:
                logging.info(f'Uploaded image file from user {message.chat.id}')

                get_file_api_url = f'https://api.telegram.org/bot{BOT_TOKEN}/getFile'
                get_file_content_api_url = f'https://api.telegram.org/file/bot{BOT_TOKEN}/'
                response = requests.post(get_file_api_url, params={'file_id': message.document.file_id})
                try:
                    json_data = json.loads(response.content)
                    response = requests.get(url=get_file_content_api_url + f"{json_data['result']['file_path']}")
                    image_type = message.document.mime_type.split(sep='/')[1]
                    photo_path = pathlib.Path('data', str(message.chat.id), 'documents',
                                          f"img_{data['curr_photos_count']}."
                                          f"{image_type}")
                    with open(photo_path, 'wb') as file:
                        file.write(response.content)
                        logging.info("File downloaded successfully")
                except KeyError:
                    logging.info(f"Can't download file {message.document.file_id} "
                                 f"with {message.document.file_size} size")
                    data['curr_photos_count'] -= 1
                    await message.answer(text=''.join(get_key_error_text(message)))


async def process_download_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if data['curr_photos_count'] <= MAX_PHOTOS_COUNT:
            logging.info(f"Uploaded photo from user {message.chat.id}")
            photo = message.photo.pop()
            await photo.download(destination_dir=pathlib.Path('data', str(message.chat.id)))
        else:
            text = maximum_photos_count_text()
            await message.answer('\n'.join(text), reply_markup=keyboard_sending_photo_state)
