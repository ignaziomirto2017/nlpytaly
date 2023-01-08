import inspect
from typing import List

from ...Tag import Tag
from .SemRole.SemRole import AbstractSemRole


def pred_is_marked(x: Tag):
    res = any(x.startswith("PRED") for x in dir(x))
    return res


def print_all(obj: object):
    for key in dir(obj):
        if not key.startswith("_"):
            print(key, getattr(obj, key))


def list_equals_no_order(list1: List, list2: List):
    for item in list1:
        print("is", item, "in", list2, "?", item in list2)
        assert item in list2
    for item in list2:
        print("is", item, "in", list1, "?", item in list1)
        assert item in list1


def assign_and_increment(
    t: Tag, semantic_role: AbstractSemRole, semantic_roles: List[AbstractSemRole]
):
    # no "Mario era bello"
    if semantic_role.f2[0] == "ESSERE":
        return

    if True:
        curframe = inspect.currentframe()
        calframe = inspect.getouterframes(curframe, 2)
        print(
            f"Assigned SemRole: {calframe[1].function}:{calframe[1].lineno} from tag {t}"
        )

    if t.can_assign_sem_roles():
        semantic_roles.append(semantic_role)
        t.inc_assigned_sem_roles()
