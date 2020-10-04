from typing import List

from ..Tag import Tag
from ..data.correzioni_occorrenza import correzioni_occorrenza_


# occorrenza: (pos, lemma, genere, numero, persona)
def correzioni_occorrenza(tags: List[Tag]) -> None:
    for t in tags:
        if t._occorrenza in correzioni_occorrenza_:
            for i, item in enumerate(correzioni_occorrenza_[t._occorrenza]):
                if i == 0 and item is not None:
                    t.pos = item
                if i == 1 and item is not None:
                    t.lemma = item
                if i == 2 and item is not None:
                    t.set_g(item)
                if i == 3 and item is not None:
                    t.set_n(item)
                if i == 4 and item is not None:
                    t.set_p(item)
