import sys
from loguru import logger as loguru_logger


def filter_level(level):
    def fn(m):
        return m["level"] == level

    return fn


def config_logger():
    loguru_logger.remove()
    handlers = [
        {
            "sink": sys.stdout,
            "colorize": True,
            "format": "<level>{level}</level> | {message}",
            "level": "INFO",
            "backtrace": False,
        },
        {
            "sink": "./logs/app_error.log",
            "format": "{time:YY-MM-DD HH:mm:ss} - {message}",
            "level": "ERROR",
        },
    ]
    loguru_logger.configure(handlers=handlers)

    return loguru_logger


logger = config_logger()
