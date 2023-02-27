import os
import logging
import functools
import traceback
import os

from bench.common.config import Config
from logging.handlers import TimedRotatingFileHandler

logger = logging.getLogger(__name__)

def _initLogger():
    logger.setLevel(Config.LOGFILE_LEVEL)

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(Config.CONSOLE_LEVEL)
    console_handler.setFormatter(logging.Formatter(
        "[%(levelname)s] %(asctime)s: %(message)s"))

    # Log file Handler
    file_handler = TimedRotatingFileHandler(
        filename    = Config.LOGFILE_PATH,
        when        = 'D',
        interval    = Config.LOGFILE_INTERVAL,
        backupCount = Config.LOGFILE_BACKUP_COUNT
    )
    file_handler.setLevel(Config.LOGFILE_LEVEL)
    file_handler.setFormatter(logging.Formatter(
        "[%(levelname)s] %(asctime)s: %(message)s"))

    # Error log file Handler
    error_handler = TimedRotatingFileHandler(
        filename    = Config.LOGFILE_PATH + '.error',
        when        = 'D',
        interval    = Config.LOGFILE_INTERVAL,
        backupCount = Config.LOGFILE_BACKUP_COUNT
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(logging.Formatter(
        "[%(levelname)s] %(asctime)s: %(message)s"))
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.addHandler(error_handler)

try:
    _initLogger()
except PermissionError:
    print("[PERMISSION ERROR] NO Permissions to init Log File!")
    os._exit(0)

CALL_LEVEL = -1
PLACEHOLDER = " " * 4