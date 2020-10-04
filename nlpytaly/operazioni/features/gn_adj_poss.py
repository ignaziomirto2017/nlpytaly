from typing import List

from ...Tag import Tag


def gn_poss_adj(tags: List[Tag]) -> None:
    for t in tags:
        if t.pos == "PRO:poss":
            if t.occ.endswith("oro"):
                t.set_gn("", "p")
                t.set_p(3)
            elif t.occ.endswith("o"):
                t.set_gn("m", "s")
                if t.occ.endswith("io"):
                    t.set_p(1)
                elif t.occ == "tuo":
                    t.set_p(2)
                elif t.occ == "suo":
                    t.set_p(3)
                elif t.occ == "nostro":
                    t.set_p(1)
                elif t.occ == "vostro":
                    t.set_p(2)
            elif t.occ.endswith("a"):
                t.set_gn("f", "s")
                if t.occ.endswith("ia"):
                    t.set_p(1)
                elif t.occ == "tua":
                    t.set_p(2)
                elif t.occ == "sua":
                    t.set_p(3)
                elif t.occ == "nostra":
                    t.set_p(1)
                elif t.occ == "vostra":
                    t.set_p(2)
            elif t.occ.endswith("i"):
                t.set_gn("m", "p")
                if t.occ.endswith("iei"):
                    t.set_p(1)
                elif t.occ == "tuoi":
                    t.set_p(2)
                elif t.occ == "suoi":
                    t.set_p(3)
                elif t.occ == "nostri":
                    t.set_p(1)
                elif t.occ == "vostri":
                    t.set_p(2)
            elif t.occ.endswith("e"):
                t.set_gn("f", "p")
                if t.occ == "mie":
                    t.set_p(1)
                elif t.occ == "tue":
                    t.set_p(2)
                elif t.occ == "sue":
                    t.set_p(3)
                elif t.occ == "nostre":
                    t.set_p(1)
                elif t.occ == "vostre":
                    t.set_p(2)
