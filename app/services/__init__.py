from aiohttp import web

from . import apscheduler


def setup(app: web.Application) -> None:
    apscheduler.setup(app)
