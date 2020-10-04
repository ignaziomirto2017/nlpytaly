from typing import List

from ...Tag import Tag


def gn_pp(tags: List[Tag]) -> None:
    for t in tags:
        if t.pos == "VER:pper":
            if t.occ.endswith("o"):
                t.set_gn("m", "s")
            elif t.occ.endswith("a"):
                t.set_gn("f", "s")
            elif t.occ.endswith("i"):
                t.set_gn("m", "p")
            elif t.occ.endswith("e"):
                t.set_gn("f", "p")
