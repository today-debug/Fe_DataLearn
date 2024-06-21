import typing as t
from queue import PriorityQueue

import numpy as np

from .utils import get_logger

__logger = get_logger(name=__file__)


def check_input(x: np.ndarray, y: np.ndarray):
    if len(x) != len(y):
        __logger.error("Inconsistent input data")
        raise RuntimeError("Inconsistent input data")


def minkowski_distance(x: np.ndarray, y: np.ndarray, p: int = 2):
    """
        if p = 1,it is equivalent to Manhattan_Distance;
        if p = 2,it is equivalent to Euclidean_Distance;
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


def nearest(dataset: np.ndarray,
            k: int = 1,
            target: int = 0,
            func: t.Callable = minkowski_distance
            ) -> list[tuple[np.ndarray, int, float]]:
    """
        k: 返回最邻近点的数量
        target: 聚类中心点在data数组中的下标
        func: 距离计算方式

        return:
            list[(data,index,distance)]
    """
    if k > len(dataset) - 1:
        __logger.error(
            "k is larger than len(dataset)!!!\nPlease check your input.")
    if k == len(dataset) - 1:
        return np.concatenate((dataset[:target], dataset[target + 1:]))

    center = dataset[target]
    pq: PriorityQueue[tuple[int, float]] = PriorityQueue()
    for i in range(0, len(dataset)):
        if i == target:
            continue
        dis_idx: tuple = (func(dataset[i], center), i)
        pq.put(dis_idx)

    k_nearest_dataset: list = []
    for i in range(0, k):
        data = pq.get()
        k_nearest_dataset.append((dataset[data[1]], data[1], data[0]))

    return k_nearest_dataset


# dataset = np.array([[1,3],[2,4],[7,5],[10,3],[2,4]])
# res = nearest(dataset,k = 4)
# import pdb;pdb.set_trace()
