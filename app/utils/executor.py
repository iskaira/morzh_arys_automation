import asyncio

from aiogram import Dispatcher
from aiohttp import web
from loguru import logger


async def on_startup(app: web.Application):
    dp = app["dp"]
    bot = app["bot"]
    asyncio.create_task(dp.start_polling(reset_webhook=True))
    bot_info = await bot.get_me()
    logger.info(f"\n"
                f"username @{bot_info['username']}\n"
                f"name {bot_info['first_name']})\n"
                f"ID: {bot_info['id']}")


async def on_shutdown(app: web.Application):
    app_dp: Dispatcher = app["dp"]
    await app_dp.storage.close()
    await app_dp.storage.wait_closed()


def setup(app: web.Application):
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
