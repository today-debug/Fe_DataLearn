import numpy as np
from frequent_item import get_frequent_items
from rules import get_rules


def main(dataset: np.ndarray, thres: int, conf: float):
    frequent_items = get_frequent_items(dataset, thres)
    rules = get_rules(frequent_items, conf)

    return rules


if __name__ == "__main__":
    main()
