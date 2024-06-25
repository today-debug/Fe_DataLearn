import numpy as np


def get_frequent_items(dataset, thres: int):
    pass


def a_prior(dataset: list[list], thres: int):
    one_tuple: dict = {}
    for data in dataset:
        for i in data:
            if i not in one_tuple.keys():
                one_tuple.update({i: 1})
            else:
                one_tuple.update({i: (one_tuple.get(i) + 1)})

    one_frequent_items: dict = {}
    one_frequent_keys: list = []
    for key, val in one_tuple.items():
        if val >= thres:
            one_frequent_items.update({key: val})
            one_frequent_keys.append(key)

    frequent_items = sub_a_prior(dataset, thres, one_frequent_items,
                                 one_frequent_keys)
    frequent_items.update(one_frequent_items)
    return frequent_items


def sub_a_prior(dataset: list[list], thres: int, frequent_item: dict,
                one_frequent_keys: list):
    """
        frequent_item:上一层处理好的k-tuple频繁项集合
        k = len(candidate_items[0])
    """

    #迭代终止条件 len(candidate_item) == max(len(dataset.iter())) or 无k-tuple频繁项
    candidate_items = generate_candidate(frequent_item, one_frequent_keys)

    k_candidate_items: dict = {}
    for data in dataset:
        for item in candidate_items:
            if len(data) < len(set(data) | set(item)):
                continue
            cnt = k_candidate_items.get(item) + 1 if k_candidate_items.get(
                item) else 1
            k_candidate_items.update({item: cnt})

    k_frequent_items: dict = {}
    for key, val in k_candidate_items.items():
        if val >= thres:
            k_frequent_items.update({key: val})

    if k_frequent_items:
        k1_frequent_items = sub_a_prior(dataset, thres, k_frequent_items,
                                        one_frequent_keys)
        k_frequent_items.update(k1_frequent_items)

    return k_frequent_items


def generate_candidate(frequent_item: dict, one_frequent_keys: list):
    k = len(next(iter(frequent_item)))

    candidate_item = []
    for item in frequent_item.keys():
        for one_item in one_frequent_keys:
            candidate_set = set(item) | set(one_item)
            if len(candidate_set) < k + 1:
                continue
            candidate_item.append(list(candidate_set))
    return candidate_item


def get_rules(frequent_items: dict[list, float], conf: float):
    """
        item(frequent_items.iter()): (["a","b"],frequency)
    """
    rules = []
    for val, fre in frequent_items.items():  #[a,b]
        for tval, _ in frequent_items.items():  #[c,d]
            all_val = set(val) | set(tval)
            if len(all_val) < len(val) + len(tval):  #判断是否有重复元素
                continue

            tfre = frequent_items.get(list(all_val))  #[a,b,c,d]
            if tfre / fre > conf:  # p(a,b,c,d) / p(a,b)
                rules.append((val, tval))

    return rules
