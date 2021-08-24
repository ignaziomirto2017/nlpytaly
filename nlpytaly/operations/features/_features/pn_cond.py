from typing import List

from ....Tag import Tag


def pn_cond(tags: List[Tag]) -> None:
    """
    Person and number for "condizionale"
    """
    for t in tags:
        if t.pos == "VER:cond":
            if t.occ.endswith("rei"):
                t.set_pn(1, "s")
            elif t.occ.endswith("resti"):
                t.set_pn(2, "s")
            elif t.occ.endswith("rebbe"):
                t.set_pn(3, "s")
            elif t.occ.endswith("remmo"):
                t.set_pn(1, "p")
            elif t.occ.endswith("reste"):
                t.set_pn(2, "p")
            elif t.occ.endswith("rebbero"):
                t.set_pn(3, "p")
