from typing import List

from ....Tag import Tag


def gn_prep_art(tags: List[Tag]) -> None:
    """
    Gender and number for "preposizioni articolate"
    """
    for t in tags:
        if t.pos == "PRE:det":
            if t.occ.endswith("o"):  # dello
                t.set_gn("m", "s")
            elif t.occ.endswith("a"):  # della
                t.set_gn("f", "s")
            elif t.occ.endswith("e"):  # delle
                t.set_gn("f", "p")
            elif t.occ.endswith("i"):  # dei, degli
                t.set_gn("m", "p")
            elif t.occ.endswith("l"):  # del
                t.set_gn("m", "s")
            elif t.occ.endswith("l'"):  # dell'
                t.set_gn("m|f", "s")
            t.set_p(3)
