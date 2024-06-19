import typing as t

import numpy as np
from utils import get_logger

__logger = get_logger(name=__file__)


def check_input(x: np.ndarray, y: np.ndarray):
    if len(x) != len(y):
        __logger.error("Inconsistent input data")
        raise RuntimeError("Inconsistent input data")


def minkowski_distance(x: np.ndarray, y: np.ndarray, p: int = 2):
    """
        if p = 1,it is equivalent to Manhattan_Distance
        if p = 2,it is equivalent to Euclidean_Distance
        if p -> ∞,it is equivalent to Chebyshev_Distance
    """
    check_input(x, y)
    return np.power(np.sum(np.abs(x - y)**p), 1 / p)


def chebyshev_distance(x: np.ndarray, y: np.ndarray):
    check_input(x, y)
    return np.max(np.abs(x - y))


def cosine(x: np.ndarray, y: np.ndarray):
    check_input(x, y)

    # 计算数据向量的模
    norm_x = np.linalg.norm(x)
    norm_y = np.linalg.norm(y)

    # 返回数据 弧度距离
    return np.arccos(np.dot(x, y) / (norm_x * norm_y))


def correlation_distance(x: np.ndarray, y: np.ndarray):
    check_input(x, y)
    return 1 - np.corrcoef(x, y)[0][1]
