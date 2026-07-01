import logging
from logging.handlers import RotatingFileHandler
import sys
from pathlib import Path


LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)


# File handler (rotation)
def _create_handler(file_name, level=logging.INFO):
    handler = RotatingFileHandler(
        LOG_DIR / file_name,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=7,
    )
    handler.setLevel(level)
    return handler


def get_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    #  Set Custom Format
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )
    #                         Output log
    #     2026-06-17 |     INFO      |   auth   | user created

    #  Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    # main log
    file_handler = _create_handler("app.log")
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


def get_error_logger():
    logger = logging.getLogger("error")
    logger.setLevel(logging.ERROR)

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    handler = _create_handler("error.log", logging.ERROR)
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger
