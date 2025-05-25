import logging
import os
from logging.handlers import RotatingFileHandler

LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

LOG_FILE_PATH = os.path.join(LOG_DIR, "app.log")
ERROR_LOG_FILE_PATH = os.path.join(LOG_DIR, "error.log")
LOGGING_LEVEL = logging.INFO
LOGGING_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

logging.basicConfig(level=LOGGING_LEVEL, format=LOGGING_FORMAT)

file_handler = RotatingFileHandler(
    LOG_FILE_PATH, maxBytes=5242880, backupCount=5)
file_handler.setLevel(LOGGING_LEVEL)
file_handler.setFormatter(logging.Formatter(LOGGING_FORMAT))

error_file_handler = RotatingFileHandler(
    ERROR_LOG_FILE_PATH, maxBytes=5242880, backupCount=5)
error_file_handler.setLevel(logging.ERROR)
error_file_handler.setFormatter(logging.Formatter(LOGGING_FORMAT))

logger = logging.getLogger("")
logger.addHandler(file_handler)
logger.addHandler(error_file_handler)
