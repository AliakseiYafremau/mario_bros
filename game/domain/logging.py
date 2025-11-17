import logging


def get_logger(name: str, layer: str) -> logging.Logger:
    logger = logging.getLogger(name)

    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        (
            f"[{layer}] [%(levelname)s] [%(asctime)s] "
            "[%(module)s:%(funcName)s:%(lineno)s] - %(message)s"
        ),
    )

    console_handler = logging.FileHandler(filename="app.log")
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger
