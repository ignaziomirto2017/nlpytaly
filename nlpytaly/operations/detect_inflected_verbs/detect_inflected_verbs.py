from typing import List

from ...data.improper_predicates import improper_predicates
from ...data.verbs.auxiliaries import auxiliaries
from ...data.verbs.inflected_verbs_pos import inflected_verbs_pos
from ...Tag import Tag


def mark_aux(item: List[int], tags: List[Tag]) -> None:
    mv = "Main verb"
    aux = "AUX"
    tmp = [tags[i] for i in item if tags[i].is_verb()]
    if len(tmp) == 0:
        pass
    elif len(tmp) == 1:
        tmp[0].note = mv
    elif len(tmp) == 2:
        if tmp[0].lemma in auxiliaries:
            tmp[0].note = aux
            tmp[0].set_max_assignable_sem_roles(0)
    else:
        if tmp[0].lemma in auxiliaries:
            tmp[0].note = aux
            tmp[0].set_max_assignable_sem_roles(0)
        if tmp[1].lemma in auxiliaries:
            tmp[1].note = aux
            tmp[1].set_max_assignable_sem_roles(0)


def mark_neg(item: List[int], tags: List[Tag]) -> None:
    tmp = tags[item[0]].lemma
    if tmp == "non":
        tmp_tags = [tags[i] for i in item]
        for t in tmp_tags:
            t._is_neg_sv = True


def detect_inflected_verbs(tags: List[Tag], indexes_proclisi):
    indexes: List[List[int]] = []
    indexes_done = set()
    for t in tags:
        if t.is_inflected_verb() and t.index not in indexes_done:
            indexes.append(list())
            indexes_done.add(t.index)
            indexes[-1].append(t.index)
            for i in range(t.index + 1, len(tags)):
                if tags[i].is_adverb() or (
                    tags[i].is_verb()
                    and tags[i].lemma not in improper_predicates
                    and tags[i].pos not in inflected_verbs_pos
                ):
                    indexes[-1].append(tags[i].index)
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
        " ".join(tags[i]._occurrence for i in item) for item in indexes_proclisi_sv
    ]

    for list_ in indexes_proclisi_sv:
        for index in list_:
            index: int
            tags[index]._is_inflected_verb = True
    for item in indexes_proclisi_sv:
        mark_neg(item, tags)
    return wording_proclisi_sv, indexes_proclisi_sv
