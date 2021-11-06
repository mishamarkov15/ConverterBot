from aiogram import types


keyboard_sending_photo_state = types.ReplyKeyboardMarkup(
    keyboard=[
        [
            types.KeyboardButton(text='Конвертировать')
        ],
        [
            types.KeyboardButton(text='Отмена')
        ]
    ],
    resize_keyboard=True
)