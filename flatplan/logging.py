import logging
from typing import Optional


def setup_logger(name: str, debug: Optional[bool] = False) -> logging.Logger:
    logger = logging.getLogger(name)
    level = "DEBUG" if debug else "INFO"

    try:
        import coloredlogs

        coloredlogs.install(level=level, logger=logger)
    except ImportError:
        handler = logging.StreamHandler()
        handler.setLevel(level)
        formatter = logging.Formatter("")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(level)

    return logger
