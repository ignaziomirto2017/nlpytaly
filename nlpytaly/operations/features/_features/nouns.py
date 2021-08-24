from typing import List

from ....Tag import Tag


def nouns(tags: List[Tag]) -> None:
    """
    Gender and number for nouns
    """
    for t in tags:
        if t.pos == "NPR":
            t.set_pn(3, "s")
        elif t.pos == "NOM":
            t.set_p(3)
            if t.occ.endswith("o") and t.lemma.endswith("o") and t.lemma != "mano":
                t.set_gn("m", "s")
            elif t.occ.endswith("a") and t.lemma.endswith("o"):
                t.set_gn("f", "s")
            elif t.occ.endswith("i") and t.lemma.endswith("o") and t.lemma != "mano":
                t.set_gn("m", "p")
            elif t.occ.endswith("i") and t.lemma.endswith("a"):
                t.set_gn("m", "p")
            # obiezioni, canzone
            elif t.occ.endswith("ni") and t.lemma.endswith("ne"):
                t.set_gn("f", "p")
            elif t.occ.endswith("i") and t.lemma.endswith("e"):  # agenti
                t.set_gn("m", "p")
            elif t.occ.endswith("i") and t.lemma.endswith("i"):  # ipotesi
                t.set_gn("f", "s|p")
            elif t.occ.endswith("e") and t.lemma.endswith("o"):
                t.set_gn("f", "p")
            elif t.occ.endswith("e") and t.lemma.endswith("a"):
                t.set_gn("f", "p")
            elif t.occ.endswith("e") and t.lemma.endswith("a"):
                t.set_gn("f", "p")
            elif t.occ.endswith("ore"):
                t.set_gn("m", "s")
            elif t.occ.endswith("ente"):  # penitente
                # t.set_gn("m|f", "s")
                t.set_n("s")
            elif t.occ.endswith("enti"):  # penitenti
                # t.set_gn("m|f", "p")
                t.set_n("p")
            elif t.occ.endswith("tori"):
                t.set_gn("m", "p")
            elif t.occ.endswith("trici"):
                t.set_gn("f", "p")
            elif t.occ.endswith("essa"):
                t.set_gn("f", "s")
            elif t.occ.endswith("esse"):
                t.set_gn("f", "p")
            elif t.occ.endswith("ione"):
                t.set_gn("f", "s")
            elif t.occ.endswith("zioni"):
                t.set_gn("f", "p")
            elif t.occ.endswith("o"):
                t.set_n("s")
            elif t.occ.endswith("a"):
                t.set_gn("f", "s")
