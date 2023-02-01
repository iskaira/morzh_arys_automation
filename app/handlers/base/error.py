from aiogram.types import Update
from loguru import logger


async def errors_handler(update: Update, exception: BaseException):
    description = f"e: {type(exception).__name__}: {exception}."
    logger.exception(description, extra=update.to_python())
    return True
