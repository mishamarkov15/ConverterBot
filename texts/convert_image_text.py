import types

from aiogram import types
from aiogram.utils import markdown

from config import MAX_PHOTOS_COUNT


def command_convert_image_text() -> list:
    text = [
        "Отправьте мне фото.",
        f"Всего можно отправить до {MAX_PHOTOS_COUNT} фото.",
    ]
    return text


def cancel_convert_image_text() -> list:
    text = [
        "Процесс конвертирования отменён.",
        "Чтобы начать его заново введите команду /convert.",
    ]
    return text


def maximum_photos_count_text() -> list:
    text = [
                "Отправлено максимальное количество фотографий.",
                "Нажмите кнопку 'Конвертировать'.",
            ]
    return text


def get_key_error_text(message: types.Message) -> list:
    text = [
        f"Упс... Не удалось загрузить файл - {markdown.hbold(message.document.file_name)}."
        f" Скорее всего, он слишком много весит.\n"
        f"Загрузка остальных файлов продолжится, можете не беспокоиться."
    ]
    return text
