### logger class for sqrt product ###
import logging
import logging.handlers
import os
import datetime


LOGGING_DIR = os.environ.get("LOGGING_DIR", "/live/share/log")


class SqRTLogger:
    def __init__(
        self,
        dir_name: str = "test",
        log_file_name: str = "log",
        max_mb: int = 10,
        max_backup_count: int = 10,
        logging_dir=LOGGING_DIR,
    ):
        log_path = os.path.join(logging_dir, dir_name)

        if not os.path.exists(log_path):
            print(f"There is no log directory: {log_path}")
            print(f"Create log directory: {log_path}")
            os.makedirs(log_path, exist_ok=True)

        log_file_name = (
            f"{log_file_name}_{datetime.datetime.now().strftime('%Y%m%d')}.log"
        )

        self.max_mb = max_mb
        self.max_backup_count = max_backup_count
        self._file_path = os.path.join(log_path, log_file_name)

    def get_logger(
        self,
        logger_name: str = None,
        level: str = "DEBUG",
        file_stream: bool = True,
        console_stream: bool = True,
    ):
        logger = logging.getLogger(logger_name)

        if level == "DEBUG":
            formatter = logging.Formatter(
                "[%(asctime)s] [%(levelname)s|%(filename)s-%(funcName)s:%(lineno)s] >> %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
            logger_level = logging.DEBUG
        else:
            formatter = logging.Formatter(
                "[%(asctime)s] [%(levelname)s] >> %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
            if level == "INFO":
                logger_level = logging.INFO
            else:
                logger_level = logging.ERROR

        logger.setLevel(logger_level)

        if file_stream:
            file_handler = logging.handlers.RotatingFileHandler(
                self._file_path,
                maxBytes=self.max_mb * 1024 * 1024,
                backupCount=self.max_backup_count,
            )
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        if console_stream:
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)
            logger.addHandler(stream_handler)

        return logger
