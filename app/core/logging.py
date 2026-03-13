import sys
from loguru import logger

from app.core.config import get_config

config = get_config()


def setup_logger() -> None:
    logger.remove()

    logger.add(
        sys.stdout,
        level=config.server.LOG_LEVEL,
        format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <7}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        colorize=True,
        backtrace=True,
        diagnose=True,
        enqueue=True,
    )

    logger.add("logs/app.log", rotation="500 MB", level=config.server.LOG_LEVEL)


setup_logger()
