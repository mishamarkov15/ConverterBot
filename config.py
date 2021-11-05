from environs import Env

env = Env()
env.read_env()

emoji = {
    'smiling_face': u'\U0001F60A',
}

BOT_TOKEN = env.str("TELEGRAM_TOKEN")
ADMINS = env.list("ADMINS")

MAX_PHOTOS_COUNT = 20