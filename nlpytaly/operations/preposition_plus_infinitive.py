from typing import List

from ..Tag import Tag
from ..data.improper_predicates import improper_predicates


def detect_prep_plus_infinitive(tags: List[Tag]):
    GV = []
    for i in range(len(tags)):
        t = tags[i]
        if t.is_infinitive():
            if tags[i - 1].is_preposition() or tags[i - 1].lemma == "dopo":
                successione_liste = [tags[i - 1].index, t.index]
                count = 1
                try:
                    if (
                        not tags[i + count].is_inflected_verb()
                        and tags[i + count].is_verb()
                        or tags[i + count].is_adverb()
                    ):
                        while (
                            "VER" in tags[i + count].pos
                            or "ADV" in tags[i + count].pos
                            and tags[i + count].lemma not in improper_predicates
                            and tags[i + count].lemma != "quanto"
                        ):
                            successione_liste.insert(count + 1, tags[i + count].index)
                            count += 1
                except IndexError:
                    pass
                GV.append(successione_liste[:])
            if tags[i - 1].lemma == "non" and tags[i - 2].is_preposition():
                successione_liste = [tags[i - 2].index, tags[i - 1].index, t.index]
                count = 1
                try:
                    if (
                        not tags[i + count].is_inflected_verb()
                        and tags[i + count].is_verb()
                        or tags[i + count].is_adverb()
                    ):
                        while (
                            "VER" in tags[i + count].pos
                            or "ADV" in tags[i + count].pos
                            and tags[i + count].lemma not in improper_predicates
                            and tags[i + count].lemma != "quanto"
                        ):
                            successione_liste.append(tags[i + count].index)
                            count += 1
                except IndexError:
                    pass
                GV.append(successione_liste[:])
    for lista in GV:
        for index in lista:
            t = tags[index]
            t.diathesis = "MIDDLE_PR" if t.occ.endswith("si") else "ACTIVE"
    return GV
