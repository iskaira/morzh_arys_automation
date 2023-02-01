from aiogram import Dispatcher
from loguru import logger

from .main import start, admin_screenshots, free_pcs, admin_screenshots_directory, admin_screenshots_file
from .error import errors_handler
from ...keyboards.inline.callbacks import main_menu_cd, admin_screenshots_menu_cd, admin_screenshots_cd, back_callback
from ...keyboards.inline.menu import menu_dict
from ...keyboards.text import free_pcs as free_pcs_kb, admin_screenshots as admin_screenshots_kb
from ...states.main import LIST_DIRECTORY, START


def setup(dispatcher: Dispatcher) -> None:
    logger.info(f"setup.handlers.base.dispatcher: {dispatcher}")
    dispatcher.register_errors_handler(errors_handler)
    dispatcher.register_message_handler(start, commands=["start"], state="*")
    dispatcher.register_callback_query_handler(start, back_callback.filter(
        to=START), state="*")
    dispatcher.register_callback_query_handler(free_pcs, main_menu_cd.filter(menu_id=menu_dict[free_pcs_kb]), state="*")
    dispatcher.register_callback_query_handler(admin_screenshots, main_menu_cd.filter(
        menu_id=menu_dict[admin_screenshots_kb]), state="*")
    dispatcher.register_callback_query_handler(admin_screenshots, back_callback.filter(
        to=LIST_DIRECTORY), state="*")
    dispatcher.register_callback_query_handler(admin_screenshots_directory, admin_screenshots_menu_cd.filter(),
                                               state="*")
    dispatcher.register_callback_query_handler(admin_screenshots_file, admin_screenshots_cd.filter(),
                                               state="*")



