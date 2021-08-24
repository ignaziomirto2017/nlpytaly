from typing import List

from ..Tag import Tag
from ..data.correction_by_occurrence import correction_by_occurence_data


# occorrenza: (pos, lemma, genere, numero, persona)
def occurence_corrections(tags: List[Tag]) -> None:
    for t in tags:
        if t._occurrence in correction_by_occurence_data:
            for i, item in enumerate(correction_by_occurence_data[t._occurrence]):
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
