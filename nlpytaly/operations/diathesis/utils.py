from typing import List

from ...Tag import Tag


def assign(tags: List[Tag], t: Tag, diathesis: str):
    if not t.has_diathesis():
        for i in t.get_same_block_indexes():
            tags[i].diathesis = diathesis
