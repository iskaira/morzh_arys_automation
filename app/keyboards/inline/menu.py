from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from ..text import admin_screenshots, free_pcs, back_button
from .callbacks import main_menu_cd, admin_screenshots_menu_cd, admin_screenshots_cd, back_callback
from ...states.main import LIST_DIRECTORY, START

menu_dict = {
    free_pcs: "1",
    admin_screenshots: "2"
}


def inline_menu(row_width: int = 1):
    kb = InlineKeyboardMarkup(row_width=1)
    for k, v in menu_dict.items():
        kb.insert(InlineKeyboardButton(text=k, callback_data=main_menu_cd.new(menu_id=v)))
    return kb


def admin_screenshots_menu(dirs: list, row_width: int = 2):
    kb = InlineKeyboardMarkup(row_width=row_width)
    for directory in dirs[:20]:
        kb.insert(InlineKeyboardButton(text="📂 " + directory,
                                       callback_data=admin_screenshots_menu_cd.new(directory=directory)))
    kb.insert(InlineKeyboardButton(text=back_button,
                                   callback_data=back_callback.new(to=START)))
    return kb


def admin_screenshots_files(files: list, row_width: int = 4):
    kb = InlineKeyboardMarkup(row_width=row_width)
    for file in files:
        kb.insert(InlineKeyboardButton(text=file,
                                       callback_data=admin_screenshots_cd.new(file=file)))
    kb.insert(InlineKeyboardButton(text=back_button,
                                   callback_data=back_callback.new(to=LIST_DIRECTORY)))
    return kb
