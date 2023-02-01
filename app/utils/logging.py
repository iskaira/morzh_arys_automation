import logging
import sys
from pathlib import Path

from loguru import logger

from app import config


class InterceptHandler(logging.Handler):
    LEVELS_MAP = {
        logging.CRITICAL: "CRITICAL",
        logging.ERROR: "ERROR",
        logging.WARNING: "WARNING",
        logging.INFO: "INFO",
        logging.DEBUG: "DEBUG",
    }

    def _get_level(self, record):
        return self.LEVELS_MAP.get(record.levelno, record.levelno)

    def emit(self, record):
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(self._get_level(record), record.getMessage())


def setup():
    logger.add(
        sys.stderr,
        format="{time} {level} {message}",
        filter=config.PROJECT_LOG_NAME,
        level="INFO",
        enqueue=True,
    )
    logger.add(
        Path(config.LOGS_BASE_PATH) / f"file_{config.PROJECT_LOG_NAME}.log",
        rotation="100 mb",
        enqueue=True,
    )

    logging.basicConfig(handlers=[InterceptHandler()], level=logging.INFO)
    logger.disable("sqlalchemy.engine.base")
