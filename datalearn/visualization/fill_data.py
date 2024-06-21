import typing as t

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle

from datalearn.common import distance
from datalearn.common.utils import get_logger
from datalearn.preprocess.fill_data import LOF

__logger = get_logger(name=__file__)


def visual_LOF(dataset: np.ndarray,
               k: int = 3,
               func: t.Callable = distance.minkowski_distance,
               output: t.Optional[str] = "LOF.jpg"):
    num, dim = dataset.shape
    if (dim >= 3):
        __logger.warning("数组维度过多,无法绘制有效图表,请减少数据维度.")

    fig, ax = plt.subplots()
    ax.set_aspect("equal")  # 设置坐标轴为等比例，保证圆看起来是圆的而不是椭圆

    dataset_LOF = LOF(dataset, k, func)
    dataset_range = [
        np.min(dataset) - np.max(dataset_LOF) - 10,
        np.max(dataset) + np.max(dataset_LOF) + 10
    ]

    ax.set_xlim(dataset_range)
    ax.set_ylim(dataset_range)
    for i in range(0, num):
        circle = Circle(dataset[i],
                        dataset_LOF[i],
                        fill=False,
                        edgecolor='blue')  # fill=False表示圆内部不填充颜色
        ax.add_patch(circle)
        ax.scatter(dataset[i][0], dataset[i][1], color='red', s=2,
                   zorder=5)  # s是点的大小，zorder控制层次

    ax.grid(True)
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')

    plt.savefig(output, dpi=300)


# dataset = np.array([[1, 2], [2, 5], [85, 10], [-1, 2], [3, 1], [8, 9], [0, 0]])
# visual_LOF(dataset)
