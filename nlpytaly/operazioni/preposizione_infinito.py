from typing import List

from ..Tag import Tag
from ..data.predicati_impropri import predicati_impropri


def trova_prep_piu_inf(tags: List[Tag]):
    GV = []
    for i in range(len(tags)):
        t = tags[i]
        if t.is_infinitive():
            if tags[i - 1].is_preposition() or tags[i - 1].lemma.lower() == "dopo":
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
                            and tags[i + count].lemma not in predicati_impropri
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
                            and tags[i + count].lemma not in predicati_impropri
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


def find_gerunds(tags):
    gerunds_tags = [x for x in tags if x.is_gerund()]
    for gerund in gerunds_tags:
        gerund.diathesis = "MIDDLE_PR" if gerund.occ.endswith("si") else "ACTIVE"
    return [[x.index] for x in gerunds_tags]
