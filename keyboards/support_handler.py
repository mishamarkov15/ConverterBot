from aiogram import types


support_references = types.InlineKeyboardMarkup(
    inline_keyboard=[
        [
            types.InlineKeyboardButton(text="Telegram", url="https://t.me/mikhaiil", callback_data="telegram")
        ],
        [
            types.InlineKeyboardButton(text="VK", url="https://vk.com/mikhaiil_15", callback_data="vk")
        ],
        [
            types.InlineKeyboardButton(text="mail", callback_data="mail")
        ]
    ]
)
