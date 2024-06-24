def get_rules(frequent_items: dict[list, float], conf: float):
    """
        item(frequent_items.iter()): (["a","b"],frequency)
    """
    rules = []
    for val, fre in frequent_items.items():
        for tval, tfre in frequent_items.items():
            if has_common_element(val, tval):
                continue
            if tfre / fre > conf:
                rules.append((val, tval))


def has_common_element(list1: list, list2: list):
    return len(set(list1) | set(list2)) < len(list1) + len(list2)
