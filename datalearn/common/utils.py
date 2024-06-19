import logging


def get_logger(*, name: str = "DataLearn") -> logging.Logger:
    logger = logging.getLogger(name)

    if getattr(logger, "_init_done__", None):
        return logger
    logger._init_done__ = True

    logger.setLevel(logging.INFO)
    logger.propagate = False
    # stdout logging: master only
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger
