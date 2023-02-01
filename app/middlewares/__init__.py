from aiogram import Dispatcher
from loguru import logger

from .acl import ACLMiddleware
from .db_message_middleware import DBMessageMiddleware


def setup(dispatcher: Dispatcher) -> None:
    logger.info(f"setup.middleware.dispatcher: {dispatcher}")
    dispatcher.middleware.setup(ACLMiddleware())
    dispatcher.middleware.setup(DBMessageMiddleware())

