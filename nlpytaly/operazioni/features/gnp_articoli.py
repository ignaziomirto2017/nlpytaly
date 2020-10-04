from typing import List

from ...Tag import Tag
from ...data.gn_determinanti import gn_determinanti as dict_


def gn_articoli(tags: List[Tag]) -> None:
    for t in tags:
        if t.occorrenza in dict_:
            g, n = dict_[t.occorrenza].split("+")
            t.set_gn(g, n)
            t.set_p(3)


def gn_sostantivi_successivi(tags: List[Tag]):
    """
    una danza
    una: f. s. => danza f. s.
    """
    for i, t in enumerate(tags):
        if t.is_article() or ":det" in t.pos or "PRO:demo" in t.pos:
            if i + 1 < len(tags) and tags[i + 1].pos == "NOM":
                tags[i + 1].set_gn(t.genere, t.numero)
