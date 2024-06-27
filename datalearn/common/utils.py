import functools
import logging
import sys
import time
from typing import Callable


class SkipRetryError(Exception):
    ...


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


__logger = get_logger()


def retry(count: int,
          delay: float,
          msg: str = "",
          skip_exception=SkipRetryError):
    r"""
    A decorator that used to retry a function.
    """
    assert count > 0, "retry count must be greater than 0"
    assert delay > 0, "retry perird must be greater than 0s"

    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            for retry in range(1, count):
                try:
                    result = func(*args, **kwargs)
                    return result
                except skip_exception as e:
                    exec_info = sys.exc_info()
                    e.__traceback__ = exec_info[2].tb_next
                    raise e
                except Exception as e:
                    __logger.warning(
                        f"failed to run `{func.__name__}`, attempt {retry} of {count}. msg: {msg}\n"
                        f"Exception: {str(e)}")
                time.sleep(delay)
            return func(*args, **kwargs)

        return wrapper

    return decorator
