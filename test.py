from sqrt_utils.logging import sqrt_logging


def main():
    logger_cls = sqrt_logging.SqRTLogger()

    logger = logger_cls.get_logger(logger_name="test", level="DEBUG")
    logger.debug("debug logging test")


if __name__ == "__main__":
    main()
