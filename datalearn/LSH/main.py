"""
    LSH 3 steps
    1. shingling
    2. min-hashing
    3. divide row * band
"""
import random
from copy import deepcopy
from math import floor, sqrt
from typing import Optional, Union

from datalearn.common.utils import get_logger

_logger = get_logger(name="LSH")


def shingling(Documents: list, k: int = 8):
    shingling_set: list[set] = []
    for Document in Documents:
        document_set = set()
        document_list = Document
        if isinstance(Document, str):
            document_list = list(Document)
        elif isinstance(Document, list):
            pass
        else:
            _logger.error("Unsupported Type")
            raise RuntimeWarning

        for i in range(k, len(document_list) + 1):
            if i == k:
                current_set = document_list[:k]
            else:
                del current_set[0]
                current_set.append(document_list[i - 1])
            current_list = ''.join(str(ele) for ele in current_set)
            document_set.add(current_list)
        shingling_set.append(deepcopy(document_set))

    return shingling_set


def convert_shingling_to_boolean(shingling_set: list):
    all_shingling_set = set()
    for shingling in shingling_set:
        all_shingling_set = all_shingling_set | shingling

    boolean_set = []
    for shingling in shingling_set:
        current_set = [int(s in shingling) for s in all_shingling_set]
        boolean_set.append(current_set)
    return boolean_set


def cal_sim(s1: Union[set, list], s2: Union[set, list]):
    '''
        calculate similarity
    '''
    if type(s1) != type(s2):
        _logger.error("Input Type is different!!!")
        raise RuntimeError

    if isinstance(s1, set):
        return len(s1 & s2) / len(s1 | s2)
    elif isinstance(s1, list):
        union_num = intersection_num = 0
        for i in range(len(s1)):
            if s1[i] + s2[i] > 0:
                union_num += 1
            if s1[i] + s2[i] == 2:
                intersection_num += 1
        return intersection_num / union_num


def min_hash(boolean_set: list, permute_times: Optional[int] = None):
    set_len = len(boolean_set[0])
    if not permute_times:
        permute_times = floor(sqrt(set_len))

    random_permute_set = set()
    signature_list = []
    for idx in range(permute_times):
        random_permute = random.sample(range(set_len), set_len)
        random_permute_str = ''.join(str(ele) for ele in random_permute)
        if random_permute_str in random_permute_set:
            idx -= 1
            continue
        random_permute_set.add(random_permute_str)

        signature = []
        for bs in boolean_set:
            tmp_min = len(bs)
            for i in range(len(bs)):
                if bs[i] == 0:
                    continue
                tmp_min = random_permute[
                    i] if random_permute[i] < tmp_min else tmp_min
            signature.append(tmp_min)
        signature_list.append(signature)

    return signature_list


# documents = ["append", "aboard", "docker", "jokers", "locker", "banana"]
# document2 = [[1, 2, 3, 4, 5], [2, 3, 4, 5, 6], [1, 5, 3, 6, 7],
#              [2, 4, 6, 8, 10]]
# shingling_set = shingling(documents, 2)
# boolean_set = convert_shingling_to_boolean(shingling_set)
# min_hash_set = min_hash(boolean_set)

# print(cal_sim(boolean_set[2], boolean_set[4]))
