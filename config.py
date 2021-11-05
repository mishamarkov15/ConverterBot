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
}

BOT_TOKEN = env.str("TELEGRAM_TOKEN")
ADMINS = env.list("ADMINS")

MAX_PHOTOS_COUNT = 20