from aiogram.dispatcher.filters.state import State, StatesGroup


class ConvertImage(StatesGroup):
    waiting_for_photos = State()