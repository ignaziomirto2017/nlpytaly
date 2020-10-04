from typing import List

from ...Tag import Tag


def assign(tags: List[Tag], t: Tag, diathesis: str):
    for i in t.get_same_block_indexes():
        tags[i].diathesis = diathesis
