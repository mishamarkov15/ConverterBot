import logging
import pathlib
import shutil

from aiogram import types
from aiogram.dispatcher import FSMContext


def create_folder(path_to_folder: pathlib.Path, folder_name: str):
    if not pathlib.Path(path_to_folder, folder_name).exists():
        pathlib.Path(path_to_folder, folder_name).mkdir()


async def increase_photos_count(state: FSMContext):
    async with state.proxy() as data:
        data['curr_photos_count'] += 1


def clear_memory(message: types.Message):
    shutil.rmtree(pathlib.Path('data', str(message.chat.id)))
    logging.info(f"All files deleted successfully")
