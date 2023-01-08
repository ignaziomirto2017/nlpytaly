from typing import List

from ..data.correction_by_occurrence import correction_by_occurrence_data
from ..Tag import Tag


# occorrenza: (pos, lemma, genere, numero, persona)
# oppure
# occorrenz*: (pos, lemma, *, *, persona) (es. arrivat*)
#   * = ultimo carattere
def occurence_corrections(tags: List[Tag]) -> None:
    for t in tags:
        if t.pos == "NPR":
            continue
        elif (
            t.occ in correction_by_occurrence_data
            or t.occ[:-1] + "*" in correction_by_occurrence_data
        ):
            last_char = t.occ[-1]
            if t.occ[:-1] + "*" in correction_by_occurrence_data:
                k = t.occ[:-1] + "*"
            else:
                k = t.occ

            for i, item in enumerate(correction_by_occurrence_data[k]):
                if i == 0 and item is not None:
                    t.pos = item
                if i == 1 and item is not None:
                    t.lemma = item
                if i == 2 and item is not None:
                    if item == "*":
                        item = {"a": "f", "e": "f", "o": "m", "i": "m"}[last_char]
                    t.set_g(item)
                if i == 3 and item is not None:
                    if item == "*":
                        item = {"a": "s", "e": "p", "o": "s", "i": "p"}[last_char]
                    t.set_n(item)
                if i == 4 and item is not None:
                    t.set_p(item)
