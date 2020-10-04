from typing import List

from ...Tag import Tag


def pn_clitici(tags: List[Tag]) -> None:
    for t in tags:
        if t.lemma == "mi":
            t.set_pn(1, "s")
        if t.lemma == "me":
            t.set_pn(1, "s")
        elif t.lemma == "ti":
            t.set_pn(2, "s")
        elif t.lemma == "te":
            t.set_pn(2, "s")
        elif t.lemma == "si":
            t.set_pn(3, "s|p")
        elif t.lemma == "s'":
            t.set_pn(3, "s|p")
        elif t.lemma == "se":
            t.set_pn(3, "s|p")
        elif t.lemma == "la":
            t.set_pn(3, "s")
            t.genere = "f"
        elif t.lemma == "le":
            t.set_pn(3, "p")
            t.genere = "f"
        elif t.lemma == "li":
            t.set_pn(3, "p")
            t.genere = "m"
        elif t.lemma == "lo":
            t.set_pn(3, "s")
            t.genere = "m"
        elif t.lemma == "ci":
            t.set_pn(1, "p")
        elif t.lemma == "c'":
            t.set_pn(1, "p")
        elif t.lemma == "ce":
            t.set_pn(1, "p")
        elif t.lemma == "vi":
            t.set_pn(2, "p")
        elif t.lemma == "ve":
            t.set_pn(2, "p")
        elif t.lemma == "gli":
            t.set_pn(3, "s|p")
        elif t.lemma == "loro":
            t.set_pn(3, "p")
        elif t.lemma == "io":
            t.set_pn(1, "s")
            t.note = "Sogg"
        elif t.lemma == "tu":
            t.set_pn(2, "s")
            t.note = "Sogg"
        elif t.lemma == "me":
            t.set_pn(1, "s")
            t.note = "Ogg"
        elif t.lemma == "te":
            t.set_pn(2, "s")
            t.note = "Ogg"
        elif t.lemma == "noi":
            t.set_pn(1, "p")
        elif t.lemma == "voi":
            t.set_pn(2, "p")
        elif t.lemma == "lui":
            t.set_pn(3, "s")
        elif t.lemma == "lei":
            t.set_pn(3, "s")
        elif t.lemma == "loro":
            t.set_pn(3, "p")
