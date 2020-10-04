from typing import List

from ..Tag import Tag
from ..data.predicati_impropri import predicati_impropri
from ..data.verbi.ausiliari import verbi_ausiliari
from ..data.verbi.flessi import verbi_flessi


def mark_aux(item: List[int], tags: List[Tag]) -> None:
    mv = "Main verb"
    aux = "AUX"
    tmp = [tags[i] for i in item if tags[i].is_verb()]
    if len(tmp) == 0:
        pass
    elif len(tmp) == 1:
        tmp[0].note = mv
    elif len(tmp) == 2:
        if tmp[0].lemma in verbi_ausiliari:
            tmp[0].note = aux
    else:
        if tmp[0].lemma in verbi_ausiliari:
            tmp[0].note = aux
        if tmp[1].lemma in verbi_ausiliari:
            tmp[1].note = aux


def trova_verbo_flesso(tags: List[Tag], indexes_proclisi):
    indexes: List[List[int]] = []
    indexes_done = set()
    for t in tags:
        if t.is_inflected_verb() and t.index not in indexes_done:
            indexes.append(list())
            if t.index - 1 >= 0 and tags[t.index - 1].occ == "non":
                indexes_done.add(t.index - 1)
                indexes[-1].append(t.index - 1)
                tags[t.index - 1].is_verbo_flesso = True
            indexes_done.add(t.index)
            indexes[-1].append(t.index)
            t.is_verbo_flesso = True
            for i in range(t.index + 1, len(tags)):
                if tags[i].is_adverb() or (
                    tags[i].is_verb()
                    and tags[i].lemma not in predicati_impropri
                    and tags[i].pos not in verbi_flessi
                ):
                    indexes[-1].append(tags[i].index)
                    tags[i].is_verbo_flesso = True
                    indexes_done.add(tags[i].index)
                else:
                    break
    for item in indexes:
        mark_aux(item, tags)

    indexes_proclisi_sv = list(zip(indexes_proclisi, indexes))
    for i in range(len(indexes_proclisi_sv)):
        item = indexes_proclisi_sv[i]
        indexes_proclisi_sv[i] = item[0] + item[1]
    wording_proclisi_sv = [
        " ".join(tags[i]._occorrenza for i in item) for item in indexes_proclisi_sv
    ]
    return wording_proclisi_sv, indexes_proclisi_sv
