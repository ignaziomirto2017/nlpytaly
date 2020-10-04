from typing import List

from ...Tag import Tag


def pn_impf(tags: List[Tag]) -> None:
    for t in tags:
        if t.pos == "VER:impf":
            if t.occ.endswith("vo") or t.occ == "ero":
                t.set_pn(1, "s")
            elif t.occ.endswith("vi"):
                t.set_pn(2, "s")
            elif t.occ.endswith("va") or t.occ == "era":
                t.set_pn(3, "s")
            elif t.occ.endswith("vamo"):
                t.set_pn(1, "p")
            elif t.occ.endswith("vate"):
                t.set_pn(2, "p")
            elif t.occ.endswith("vano") or t.occ == "erano":
                t.set_pn(3, "p")
