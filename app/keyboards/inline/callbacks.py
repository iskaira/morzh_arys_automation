from aiogram.utils.callback_data import CallbackData

main_menu_cd = CallbackData("main_menu", "menu_id")
admin_screenshots_menu_cd = CallbackData("admin_screenshots_menu", "directory")
admin_screenshots_cd = CallbackData("admin_screenshots", "file")
back_callback = CallbackData("back", "to")
skip_callback = CallbackData("skip", "to")
no_clb = CallbackData("no_clb", "text", "show_alert")
