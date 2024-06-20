'''
    填补空缺数据
'''
import typing as t

import numpy as np

from datalearn.common import distance


def LOF(dataset: np.ndarray,
        k: int = 2,
        func: t.Callable = distance.chebyshev_distance):
    """
        Local Outlier Factor  用于检测局部离群点
        k: 参数，决定计算的最近邻点个数
        func: 距离计算方式

        return: 各点LOF数值
    """
    """calculate lrd(Local Reachable Density)"""
    dataset_lrd = []
    for i in range(0, len(dataset)):
        k_near_points_info = distance.nearest(dataset, k, i, func)
        k_nearest_distance = k_near_points_info[-1][2]
        k_near_distance = []
        for near_point in k_near_points_info:
            k_near_distance.append(
                np.maximum(k_nearest_distance, near_point[2]))
        dataset_lrd.append(k / np.sum(k_near_distance))
    """calculate LOF"""
    dataset_lof = []
    for i in range(0, len(dataset)):
        k_near_points_info = distance.nearest(dataset, k, i, func)

        lrd_sum = 0
        for near_point in k_near_points_info:
            lrd_sum += dataset_lrd[near_point[1]]
        dataset_lof.append(lrd_sum / (dataset_lrd[i] * k))

    return np.array(dataset_lof)


# dataset = np.array([[1,2],[2,5],[85,10],[-1,2],[3,1],[8,9],[0,0]])
# res = LOF(dataset)
# import pdb;pdb.set_trace()
