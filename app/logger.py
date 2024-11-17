import logging
from logging import Logger
import coloredlogs

_log_level = logging._nameToLevel["DEBUG"]


def get_logger(name) -> Logger:
    colorlog_format = "%(asctime)s | line: %(lineno)d | %(name)s/%(funcName)s | %(levelname)s: %(message)s"
    logger = logging.getLogger(name)
    coloredlogs.install(fmt=colorlog_format, level=_log_level, logger=logger)
    return logger


log = get_logger(__name__)
