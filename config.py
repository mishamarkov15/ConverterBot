from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env.str("TELEGRAM_TOKEN")
ADMINS = env.list("ADMINS")
