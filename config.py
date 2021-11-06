from aiogram import types
from environs import Env

env = Env()
env.read_env()

emoji = {
    'left': u'\U000000AB',            #стрелка влево
    'right': u'\U000000BB',           #стрелка вправо
    'smiling_face': u'\U0001F60A',    #улыбающийся смайлик с розовыми щёчками
    'waving_hand': u'\U0001F44B',     #машущая рука
    'light_bulb': u'\U0001F4A1',      #лампочка
    'blue_diamond': u'\U0001F537',    #голубой ромб
    'camera_flash': u'\U0001F4F8',    #камера со вспышкой
    'documents': u'\U0001F4D1',       #документы
    'gear': u'\U00002699',            #шестеренка
    'multiply': u'\U000000D7',        #знак умножения
    'memo': u'\U0001F4DD',            #тетрадь с ручкой
    'outbox_tray': u'\U0001F4E4',     #отправка письма
    'pensive_face': u'\U0001F614',    #грустное лицо
}

AVAILABLE_TYPES_FOR_PHOTO = [
    'image/jpeg', 'image/pjpeg', 'image/tiff', 'image/x-tiff',
    'image/bmp', 'image/x-windows-bmp', 'image/gif', 'image/png', 'image/heic',
    'image/heif', 'image/heic-sequence', 'image/heif-sequence',
]

test = {
    "start": "Запустить бота",
    "convert_image": "Начать отправку фото",
    "settings": "Настройки",
    "help": "Вывести справку",
    "support": "Связь с поддержкой"
}


BOT_COMMANDS = [types.BotCommand(cmd, desc) for cmd, desc in test.items()]

BOT_TOKEN = env.str("TELEGRAM_TOKEN")
ADMINS = env.list("ADMINS")

MAX_PHOTOS_COUNT = 30
