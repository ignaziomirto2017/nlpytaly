from typing import List

from ....Tag import Tag


def pn_futu(tags: List[Tag]) -> None:
    """
    Person and number for "futuro"
    """
    for t in tags:
        if t.pos == "VER:futu":
            if t.occ.endswith("rò"):
                t.set_pn(1, "s")
            elif t.occ.endswith("rai"):
                t.set_pn(2, "s")
            elif t.occ.endswith("rà"):
                t.set_pn(3, "s")
            elif t.occ.endswith("remo"):
                t.set_pn(1, "p")
            elif t.occ.endswith("rete"):
                t.set_pn(2, "p")
            elif t.occ.endswith("ranno"):
                t.set_pn(3, "p")
