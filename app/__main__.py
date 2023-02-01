from aiohttp import web

from app import config
from app import misc

misc.setup()
web.run_app(misc.app)
