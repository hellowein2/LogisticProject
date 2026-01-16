import os
import sys
from loguru import logger


def setup_logging() -> None:
    logger.remove()

    level = os.getenv("LOG_LEVEL", "INFO").upper()

    logger.add(
        sys.stdout,
        level=level,
        enqueue=True,
        backtrace=True,
        diagnose=False,
        format=(
        "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level:<8} | "
        "{name}:{function}:{line} - {message} | {extra}"
    ),
    )
