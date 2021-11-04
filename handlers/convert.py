import logging
import os, os.path
import shutil, pathlib, cv2

from PIL import Image, ImageFile

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
        await increase_photos_count(state)
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


def photo2pdf(message: types.Message):
    images = []
    if pathlib.Path('data', str(message.chat.id), 'photos').exists():
        path_to_photos = pathlib.Path('data', str(message.chat.id), 'photos')
        for file in os.listdir(path_to_photos):
            images.append(Image.open(pathlib.Path(path_to_photos, str(file))).convert('RGB'))
    if pathlib.Path('data', str(message.chat.id), 'documents').exists():
        path_to_photos = pathlib.Path('data', str(message.chat.id), 'documents')
        for file in os.listdir(path_to_photos):
            im = cv2.imread(str(pathlib.Path(path_to_photos, str(file))), cv2.IMREAD_UNCHANGED)
            im = cv2.cvtColor(im, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(im)
            images.append(im)
    im1 = images[0]
    if len(images) != 0:
        im1.save(pathlib.Path('data', str(message.chat.id), 'result.pdf'),
                    save_all=True, append_images=images[1:])
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
            photo2pdf(message)
            path_to_pdf = pathlib.Path('data', str(message.chat.id), 'result.pdf')
            await message.answer_document(document=open(path_to_pdf, 'rb'), caption="Ваш PDF файл:)")
            clear_memory(message)
    await state.finish()


async def process_download_document(message: types.Message, state: FSMContext):
    if message.document.mime_type in ['image/jpeg', 'image/pjpeg', 'image/tiff', 'image/x-tiff',
                                      'image/bmp', 'image/x-windows-bmp', 'image/gif']:
        async with state.proxy() as data:
            if data['curr_photos_count'] <= MAX_PHOTOS_COUNT:
                logging.info(f'Uploaded photo from user {message.chat.id}')
                await message.document.download(destination_dir=pathlib.Path('data', str(message.chat.id)))


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
