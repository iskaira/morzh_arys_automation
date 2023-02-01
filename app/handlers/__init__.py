from aiogram import Dispatcher


def setup(dispatcher: Dispatcher) -> None:
    from . import base
    base.setup(dispatcher)
    