from aiogram import Dispatcher, types


async def set_default_commands(dp: Dispatcher):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Запустить бота"),
            types.BotCommand("convert", "Начать отправку фото"),
            types.BotCommand("settings", "Настройки"),
            types.BotCommand("help", "Вывести справку"),
            types.BotCommand("support", "Техническая поддержка")
        ]
    )