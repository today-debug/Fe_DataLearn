from typing import Optional

import numpy as np
from common.utils import get_logger, retry

_logger = get_logger("Frequent_Items")


def frequent_item(dataset: list[list], thres: int, conf: float,
                  method: Optional[str]):
    if method.capitalize() == "SAMPLE":
        _, _, sample_frequent_items = sample(dataset, thres)
        rules = get_rules(sample_frequent_items, conf)
        return rules


def get_frequent_items(dataset: list[list], thres: int):
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


@retry(count=3, delay=5)
def sample(dataset: list[list], thres: int, sampling_ratio: float) -> tuple:
    """
        sampling_ratio:采样比例
        return: (采样数据,采样数据频繁项阈值,采样数据频繁项集)
    """
    from random import random as rd
    sample_dataset = []
    for data in dataset:
        if rd() > sampling_ratio:
            continue
        sample_dataset.append(data)

    sample_thres = thres * sampling_ratio * 0.8  #0.8是经验系数，可以更改
    sample_frequent_items = get_frequent_items(sample_dataset, sample_thres)
    assert sample_check(dataset, thres, sample_frequent_items)
    return (sample_dataset, sample_thres, sample_frequent_items)


def sample_check(dataset: list[list], thres: int,
                 sample_frequent_item: dict) -> bool:
    """
        检查采样数据频繁集是否与原数据集一致
        1. sample有的,原数据集也得有
        2. 原数据集有的，sample不一定有
        总结：可以少，但不能多

        **param
        sample_XXX是采样数据的参数
        其余均为原始数据的参数
    """
    frequent_items: dict = {}
    for data in dataset:
        for key in sample_frequent_item.keys():
            if len(set(key) | set(data)) == len(data):
                cnt = frequent_items.get(key) if frequent_items.get(key) else 0
                frequent_items.update({key: (cnt + 1)})

    for key, item in frequent_items.items():
        if item < thres:
            _logger.warning(
                "Sampling Frequent Items in infrequent. Please Retry!")
            return False
    return True
