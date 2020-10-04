from typing import List

from ...Tag import Tag


def pn_congimp(tags: List[Tag]) -> None:
    for t in tags:
        if t.pos == "VER:cimp":
            if t.occ.endswith("ssi"):
                t.set_pn(1, "s")
            elif t.occ.endswith("ssi"):
                t.set_pn(2, "s")
            elif t.occ.endswith("sse"):
                t.set_pn(3, "s")
            elif t.occ.endswith("ssimo"):
                t.set_pn(1, "p")
            elif t.occ.endswith("ste"):
                t.set_pn(2, "p")
            elif t.occ.endswith("ssero"):
                t.set_pn(3, "p")
