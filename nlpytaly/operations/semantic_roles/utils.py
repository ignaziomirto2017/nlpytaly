from typing import List

from ...Tag import Tag


def pred_is_marked(x: Tag):
    res = any(x.startswith("PRED") for x in dir(x))
    return res


def list_equals_no_order(list1: List, list2: List):
    for item in list1:
        print_all(item)
        assert item in list2
    for item in list2:
        print_all(item)
        assert item in list1


def print_all(obj: object):
    for key in dir(obj):
        if not key.startswith("_"):
            print(key, getattr(obj, key))
