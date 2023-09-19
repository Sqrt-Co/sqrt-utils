### logger class for sqrt product ###
import logging
from logging.handlers import TimedRotatingFileHandler
import os

home_directory = os.path.expanduser("~")
_LOGGING_DIR = os.environ.get("LOGGING_DIR", f"{home_directory}/logs")

def get_sqrt_logger(logger_name: str = "test", log_type: str = None, log_level: str = None, logging_dir: str = _LOGGING_DIR):
    """
    will used for logging path : {logging_dir}/{log_type}/{logger_name}.log
        ex) /live/share/log/DG/upbit_downloader.log

    log_level: str (DEBUG, INFO)
        If no log level is provided, set the log level through an environment variable.
"""

    logger = logging.getLogger(logger_name)

    # if log_level is not given, set log_level by Environment Variables
    if None == log_level:
        ENVIRONMENT = os.environ.get("ENVIRONMENT")
        if "DEVELOPMENT" == ENVIRONMENT:
            log_level = logging.DEBUG
        elif None == ENVIRONMENT:
            print("Can't find ENVIRONMENT from Environment variable. Set log level to INFO")
            log_level = logging.INFO
        else:
            log_level = logging.INFO
    elif "DEBUG" == log_level.upper():
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO
    
    logger.setLevel(log_level)

    # Add a handler only if the logger has no handlers
    if not logger.handlers:

        if None == log_type:
            log_type = logger_name



        # make logging directory
        if not os.path.exists(f"{logging_dir}/{log_type}"):
            os.makedirs(f"{logging_dir}/{log_type}")

        # add handler
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s|%(filename)s-%(funcName)s:%(lineno)s] >> %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        stream_handler = logging.StreamHandler()
        timed_rotating_handler = logging.handlers.TimedRotatingFileHandler(
            f"{logging_dir}/{log_type}/{logger_name}.log",
            when="midnight",
            utc=True,
        )

        stream_handler.setFormatter(formatter)
        timed_rotating_handler.setFormatter(formatter)

        logger.addHandler(stream_handler)
        logger.addHandler(timed_rotating_handler)

    return logger
