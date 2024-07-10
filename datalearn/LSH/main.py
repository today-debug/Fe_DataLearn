"""
    LSH 3 steps
    1. shingling
    2. min-hashing
    3. hash into many buckets
"""
import random
from copy import deepcopy
from math import floor, sqrt
from typing import Dict, Optional, Union

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


def divide_into_bands(boolean_set: list, b: int, s: float, target: int):
    """
        divide boolean_set into b bands
        each band has r rows

        only if all bands are dissimilar,origin signature pairs are regarded as dissimilar.

        **params**
            b: number of bands
            s: threshold of similarity
            target: 
            boolean_set: signature of all document
    """
    set_len = len(boolean_set[0])
    r = floor(set_len / b)
    for i in range(b):
        r_range = [r * i, min(r * (i + 1), set_len)]
    return 0


def hash_into_buckets(min_hash_set: list) -> dict[str, list]:
    hash_signature: dict[str, list] = {}
    for i in range(len(min_hash_set[0])):
        min_hash = []
        for permute in min_hash_set:
            min_hash.append(permute[i])

        signature_str = ''.join(chr(i % 127) for i in min_hash)
        if signature_str in hash_signature.keys():
            val = hash_signature[signature_str]
            val.append(i)
            hash_signature.update({signature_str: val})
        else:
            hash_signature.update({signature_str: [i]})

    return hash_signature


def find_candidate_pairs(hash_signature: dict, min_hash_set: list, target: int,
                         s: float):
    target_key = []
    for permute in min_hash_set:
        target_key.append(permute[target])
    candidate_items = []

    for k, v in hash_signature.items():
        k = [ord(c) for c in k]
        cnt = 0
        for i in range(len(target_key)):
            if k[i] == target_key[i]:
                cnt += 1

        prob = cnt / len(target_key)
        if prob > s:
            candidate_items.extend(v)

    return candidate_items


# documents = ["append", "aboard", "docker", "jokers", "locker","docter" ,"banana","appearance","appearence"]
# document2 = [[1, 2, 3, 4, 5], [2, 3, 4, 5, 6], [1, 5, 3, 6, 7],
#              [2, 4, 6, 8, 10]]
# shingling_set = shingling(documents, 2)
# boolean_set = convert_shingling_to_boolean(shingling_set)
# min_hash_set = min_hash(boolean_set)
# hash_signature = hash_into_buckets(min_hash_set)
# candidate_keys = find_candidate_pairs(hash_signature,min_hash_set,2,0.4)

# # print(cal_sim(boolean_set[2], boolean_set[4]))
