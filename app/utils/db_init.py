from aiohttp import web

from app.services.db import db_init, close_connections


async def on_startup(app: web.Application):
    await db_init()


async def on_shutdown(app: web.Application):
    await close_connections()


def setup(app: web.Application):
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)