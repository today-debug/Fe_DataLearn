from copy import deepcopy
from typing import Optional

import numpy as np

from datalearn.common.utils import get_logger

_logger = get_logger(name="SVD")


def ED(A: np.ndarray):
    #Eigenvalue Decomposition(特征分解)
    row = len(A)
    col = len(A[0])
    try:
        assert row == col
    except AssertionError:
        raise RuntimeError("输入矩阵必须是方阵")

    eigenvalues, eigenvectors = np.linalg.eig(A)
    return eigenvalues, eigenvectors


def SVD(A: np.ndarray,
        descend_dimension: bool = False,
        dim: Optional[int] = None):
    A_T = np.transpose(A)  # A_T是矩阵A的转置
    AA_T = np.dot(A, A_T)  # AA_T  = A * A_T
    A_TA = np.dot(A_T, A)  #A_TA = A_T * A

    _, U = ED(AA_T)
    _, V = ED(A_TA)
    sigma = np.dot(np.transpose(U), np.dot(A, V))

    if not dim:
        dim = len(AA_T) - 1

    sigma[sigma < 1e-5] = 0
    A_norm = np.linalg.norm(A, 'fro')
    if descend_dimension:
        while True:
            sigma_sim = deepcopy(sigma)
            non_zero_min = np.min(sigma_sim[sigma_sim != 0])
            sigma_sim[sigma_sim <= non_zero_min] = 0

            A_sim = np.dot(U, np.dot(sigma_sim, np.matrix_transpose(V)))
            A_sim_norm = np.linalg.norm(A_sim, 'fro')

            cur_dim = len(sigma_sim[sigma_sim != 0])
            if abs(A_norm - A_sim_norm) / A_norm > 1e-2:
                _logger.warning(f"当前维数为{cur_dim},当前降维后矩阵与原矩阵相差较大，请考虑增加维数")
            sigma = deepcopy(sigma_sim)
            if cur_dim == dim:
                break

    return (U, sigma, V, A_sim)


# a = [[5,5,5,0,0],
#  [1,1,1,0,0],
#  [2,2,2,0,0],
#  [0,2,0,6,6],
#  [0,1,0,3,3],
#  [0,0,0,2,2]]
# (U,s,V,sim) = SVD(a,True,2)
# print(sim)

#test case
"""
[[5,5,5,0,0]
 [1,1,1,0,0]
 [2,2,2,0,0]
 [0,2,0,6,6]
 [0,1,0,3,3]
 [0,0,0,2,2]]
"""
