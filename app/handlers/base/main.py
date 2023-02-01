import logging

import loguru
from aiogram import types
from aiogram.dispatcher import FSMContext


from ...config import FilesDirectory
from ...keyboards.inline.callbacks import admin_screenshots_menu_cd, admin_screenshots_cd
from ...keyboards.inline.menu import inline_menu, admin_screenshots_menu, admin_screenshots_files
from ...keyboards.utils.try_message import try_message, safe_delete, smart_send_file
from ..utils.helper import get_dirs_list, get_files_list
from ...states import MainMenu
from ...reply_texts import WELCOME_MESSAGE, MAIN_MENU
from ...states.main import AdminPC


async def start(_: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if not current_state:
        await try_message(WELCOME_MESSAGE, state=state)
    await try_message(MAIN_MENU, state=state, reply_markup=inline_menu())
    await MainMenu.START.set()


async def free_pcs(message: types.Message, state: FSMContext):
    # await safe_delete(message)
    await try_message("В разработке free PCs /start", state=state)


async def back_to_directories(callback: types.CallbackQuery, state: FSMContext):
    message = callback.message
    await admin_screenshots(message, state)


async def admin_screenshots(message: types.Message, state: FSMContext):
    # await safe_delete(message)
    dirs = get_dirs_list()
    await try_message("Выберите дату или напишите в формате 2023-12-31", state=state,
                      reply_markup=admin_screenshots_menu(dirs))
    await AdminPC.LIST_DIRECTORY.set()


async def admin_screenshots_directory(callback: types.CallbackQuery, state: FSMContext):
    # await safe_delete(message)
    data = admin_screenshots_menu_cd.parse(callback.data)
    directory = data.get('directory')
    logging.warning(f" data: {data}")
    await state.update_data(directory=directory)
    files = get_files_list(directory)
    logging.warning(f" files: {files}")
    await try_message(f"Выберите файл {directory}", state=state,
                      reply_markup=admin_screenshots_files(files))
    await AdminPC.LIST_DIRECTORY.set()


async def admin_screenshots_file(callback: types.CallbackQuery, state: FSMContext):
    data = admin_screenshots_cd.parse(callback.data)
    file_name = data.get('file')
    state_data = await state.get_data()
    date_directory = state_data.get('directory')
    file_path = f'{FilesDirectory}//{date_directory}//{file_name}'
    print(file_path)
    await smart_send_file(state=state, file=file_path)
