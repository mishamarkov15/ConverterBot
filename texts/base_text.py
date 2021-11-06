from aiogram.utils import markdown

import config
from misc.get_username import *
from config import emoji


def start_text(message: types.Message) -> list:
    text = [
        f" Привет, {define_username(message)}! {emoji['waving_hand']}\n\n",
        f"{emoji['blue_diamond']} {markdown.hbold('Чтобы быстро начать конвертацию')}:\n",
        f"1. Нажмите /convert_image.\n",
        f"2. Отправьте фотографии.\n"
        f"3. Нажмите на кнопку {emoji['left']}{'Конвертировать'}{emoji['right']} "
        f"или пришлите это сообщение текстом.\n\n",
        f"{emoji['blue_diamond']} {markdown.hbold('Чтобы получить список всех функций')}, нажмите /help.",
    ]
    return text


def help_text() -> list:
    text = [
        f"{emoji['light_bulb']} {markdown.hbold('Давайте расскажу, с чем я умею работать')}\n\n\n",
        f"{markdown.hbold('1. Фотографии')} {emoji['camera_flash']}\n\n",
        f"Я умею конвертировать изображения, любого формата",
        f" отправленные файлом или просто как отдельное фото. Чтобы конвертировать фото в PDF, следуйте инструкции:\n",
        f" - Нажмите /convert_image\n - Отправьте фото\n",
        f" - Нажмите на кнопку {emoji['left']}Конвертировать{emoji['right']}\n\n",
        f"{markdown.hbold('2. Документы')} {emoji['documents']}\n\n",
        f"С моей помощью можно конвертировать .docx в PDF\n\n",
        f"{emoji['blue_diamond']} {markdown.hbold('Дополнительные возможности')}\n\n\n",
        f"{markdown.hbold('1. Настройки')} {emoji['gear']}\n",
        f"Вы можете изменить настройки, выполнив команду /settings.\n\n",
        f"{markdown.hbold('1.1. Размер листа')}\nРазмер листа, который вы получите после конвертации фото в PDF.\n\n",
        f"{markdown.hbold('1.2. Имя получаемого файла')}\n",
        f"Если опция включена, то Вы сможете выбрать имя конвертированного файла.\n\n",
        f"{markdown.hbold('2. Связаться с поддержкой')} {emoji['outbox_tray']}\n",
        f"Вы можете получить контактные данные поддержки, выполнив команду /support."
    ]
    return text
