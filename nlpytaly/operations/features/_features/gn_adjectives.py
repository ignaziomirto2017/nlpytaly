from typing import List

from ....Tag import Tag
from ....data.cardinal_numbers import cardinal_numbers


def gn_adjectives(tags: List[Tag]) -> None:
    """
    Gender and number for adjectives
    """
    for t in tags:
        if t.is_adjective():
            if t.lemma not in cardinal_numbers:
                if t.occ[-1] in ["a"] and t.lemma[-1] == "o":
                    t.set_gn("f", "s")
                elif t.occ[-1] in ["o"] and t.lemma[-1] == "o":
                    t.set_gn("m", "s")
                elif t.occ[-1] in ["i"] and t.lemma[-1] in ["o"]:
                    t.set_gn("m", "p")
                elif t.occ[-1] in ["e"] and t.lemma[-1] in ["e"]:
                    t.number = "s"
                elif t.occ[-1] in ["i"] and t.lemma[-1] in ["e"]:
                    t.number = "p"
                elif t.occ[-1] in ["e"] and t.lemma[-1] in ["o"]:
                    t.set_gn("f", "p")
                elif t.occ[-1] in ["e"] and t.lemma[-1] in ["a"]:
                    t.set_gn("f", "p")
                elif t.occ[-1] in ["a"] and t.lemma[-1] in ["a"]:
                    t.set_gn("m|f", "s")
                elif t.occ.endswith("issimo"):
                    t.set_gn("m", "s")
                elif t.occ.endswith("issima"):
                    t.set_gn("f", "s")
                elif t.occ.endswith("issimi"):
                    t.set_gn("m", "p")
                elif t.occ.endswith("issime"):
                    t.set_gn("f", "p")
            else:
                t.set_pn(3, "p")
