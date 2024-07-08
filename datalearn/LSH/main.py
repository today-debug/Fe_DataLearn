"""
    LSH 3 steps
    1. shingling
    2. min-hashing
    3. divide row * band
"""
from copy import deepcopy

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


def cal_sim(s1: set, s2: set):
    '''
        calculate similarity
    '''
    return len(s1 & s2) / len(s1 | s2)


# documents = ["append","aboard","docker","jokers","locker","banana"]
# document2 = [[1,2,3,4,5],[2,3,4,5,6],[1,5,3,6,7],[2,4,6,8,10]]
# shingling_set = shingling(documents,2)
# print(cal_sim(shingling_set[2],shingling_set[4]))
