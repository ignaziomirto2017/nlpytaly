from typing import List

from ...Tag import Tag


def pn_impe(tags: List[Tag]) -> None:
    for t in tags:
        if t.pos == "VER:impe" and t.lemma.endswith("ere"):
            if t.occ.endswith("i"):
                t.set_pn(2, "s")
            elif t.occ.endswith("a"):
                t.set_pn(3, "s")
