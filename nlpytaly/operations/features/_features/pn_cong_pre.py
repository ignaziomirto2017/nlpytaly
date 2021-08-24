from typing import List

from ....Tag import Tag


def pn_congpre(tags: List[Tag]) -> None:
    """
    Person and number for "congiuntivo presente"
    """
    for t in tags:
        if t.pos == "VER:cpre":
            if t.occ[-1] in ["i", "a"]:
                t.set_pn(123, "s")
            elif t.occ.endswith("iamo"):
                t.set_pn(1, "p")
            elif t.occ.endswith("iate"):
                t.set_pn(2, "p")
            elif t.occ.endswith("no"):
                t.set_pn(3, "p")
