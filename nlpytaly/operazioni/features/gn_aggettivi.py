from typing import List

from ...Tag import Tag
from ...data.cardinali import cardinali


def gn_aggettivi(tags: List[Tag]) -> None:
    for t in tags:
        if t.is_adjective():
            if t.lemma not in cardinali:
                if t.occ[-1] in ["a"] and t.lemma[-1] == "o":
                    t.set_gn("f", "s")
                elif t.occ[-1] in ["o"] and t.lemma[-1] == "o":
                    t.set_gn("m", "s")
                elif t.occ[-1] in ["i"] and t.lemma[-1] in ["o"]:
                    t.set_gn("m", "p")
                elif t.occ[-1] in ["e"] and t.lemma[-1] in ["e"]:
                    t.numero = "s"
                elif t.occ[-1] in ["i"] and t.lemma[-1] in ["e"]:
                    t.numero = "p"
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
