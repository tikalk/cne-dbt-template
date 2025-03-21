import logging
import os
from logging.handlers import RotatingFileHandler

from rich.logging import RichHandler

from cli.config import ini_config

logger = logging.getLogger(__name__)

stream_handler = RichHandler(rich_tracebacks=True, show_time=False, show_path=False, markup=True)
stream_handler.setLevel(level=os.environ.get("LOGLEVEL", "NOTSET"))
formatter = logging.Formatter("%(message)s")
stream_handler.setFormatter(formatter)

logs_dir = "logs"

os.makedirs(logs_dir, exist_ok=True)
log_file_name = ini_config.get("cli", "log_file_name", fallback="cli.log")
file_handler = RotatingFileHandler(f"{logs_dir}/{log_file_name}", maxBytes=10**6, backupCount=5)
file_handler.setLevel(level=os.environ.get("FILE_LOGLEVEL", "DEBUG"))
formatter = logging.Formatter("%(asctime)s : %(levelname)s : %(name)s : %(message)s")
file_handler.setFormatter(formatter)

log_to_file_logger = logging.getLogger(__name__)
log_to_file_logger.setLevel(level="DEBUG")
log_to_file_logger.addHandler(file_handler)

global_log_level = "DEBUG"


def setup_logger(v, log_level):
    v.setLevel(level=log_level)
    v.removeHandler(file_handler)
    v.removeHandler(stream_handler)
    v.addHandler(file_handler)
    v.addHandler(stream_handler)


def setup_log(log_level):
    stream_handler.setLevel(level=log_level)
    for v in logging.Logger.manager.loggerDict.values():
        if type(v) is logging.Logger:
            if v.name.startswith("cli."):
                setup_logger(v, log_level)
