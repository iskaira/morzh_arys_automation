import asyncio
from datetime import datetime

import loguru
from loguru import logger

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.files import JSONStorage
from aiogram.types import ParseMode
from aiohttp import web

from app import config, middlewares

uptime_now = datetime.now()

app = web.Application()
loop = asyncio.get_event_loop()


bot = Bot(config.TELEGRAM_TOKEN, parse_mode=ParseMode.HTML, validate_token=True)
Bot.set_current(bot)

storage = JSONStorage(path=config.fsm_storage_path)
dp = Dispatcher(bot, storage=storage, loop=loop)

app["dp"] = dp
app["bot"] = bot


def setup() -> None:
    from app import handlers
    from app import services
    from app.utils import executor, logging, db_init

    db_init.setup(app)
    logging.setup()
    middlewares.setup(dp)
    # filters.setup(dp)
    handlers.setup(dp)
    services.setup(app)
    executor.setup(app)
