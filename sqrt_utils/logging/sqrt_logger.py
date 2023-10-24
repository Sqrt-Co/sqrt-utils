import logging
from logging.handlers import TimedRotatingFileHandler
import os

home_directory = os.path.expanduser("~")
log_dir = f"{home_directory}/logs"


def get_logger(logger_name):
    logger = logging.getLogger(logger_name)

    if len(logger.handlers) == 0:
        logger.setLevel(logging.DEBUG)

        # add handler
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s|%(filename)s-%(funcName)s:%(lineno)s] >> %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        if not os.path.exists(f"{log_dir}/{logger_name}"):
            os.makedirs(f"{log_dir}/{logger_name}")

        stream_handler = logging.StreamHandler()
        timed_rotating_handler = TimedRotatingFileHandler(
            f"{log_dir}/{logger_name}/{logger_name}.log",
            when="midnight",
            utc=True,
        )

        stream_handler.setFormatter(formatter)
        timed_rotating_handler.setFormatter(formatter)

        logger.addHandler(stream_handler)
        logger.addHandler(timed_rotating_handler)

    return logger
