from typing import List
from typing import Set

from .SemRole.SemRole import AteSemRole
from .pred_assigners import *
from ...Tag import Tag
from ...Utils import increment_blocks
from ...Utils import (
    mark_tag,
    search_da_phrase,
)
from ...data.ate_multiwords import (
    ate_multiwords,
    ate_multiwords_colpire,
    ate_multiwords_insultare,
)
from ...data.ate_multiwords import synonyms

multiwords: Set[str] = (
    set(ate_multiwords.keys()) | ate_multiwords_colpire | ate_multiwords_insultare
)


def mark_ate_suffix(tags: List[Tag]):
    for t in tags:
        if t.lemma == "prendere":
            pb_tags = t.get_prev_block_tags()
            nb_tags = t.get_next_block_tags(number_of_blocks=2)
            for tmp in pb_tags + nb_tags:
                if (
                    tmp.occ in multiwords
                    and tmp.index > 0
                    and tags[tmp.index - 1].lemma == "a"
                ):
                    # Per gestire i casi come prendere a calci = prendere a pedate
                    occ = tags[tmp.index].occ
                    if occ in synonyms:
                        occ = synonyms[occ]
                    mark_tag(t, pred_syn_ate, occ)
                    mark_tag(tags[tmp.index], pred_sem_ate, t)
                    increment_blocks(tags, tmp.index - 1, tmp.index)


def assign_ate_suffix(od, sem_roles, sogg, t, v):
    is_fare_caus = any(hasattr(x, pred_sem_fare_caus) for x in t.get_same_block_tags())
    if v in ate_multiwords:
        d = ate_multiwords
        verb = d[v]
    elif v in ate_multiwords_insultare:
        verb = "insultare"
    elif v in ate_multiwords_colpire:
        verb = "colpire"
    else:
        raise ValueError
    if t.is_active():
        if not is_fare_caus:
            sem_roles.append(
                AteSemRole(" ".join(x.occ for x in sogg), [verb, v], "ACTIVE", [v])
            )
        if od:
            sem_roles.append(
                AteSemRole(" ".join(x.occ for x in od), [verb, v], "PASSIVE", [v])
            )
    elif t.is_passive():
        sem_roles.append(
            AteSemRole(" ".join(x.occ for x in sogg), [verb, v], "PASSIVE", [v])
        )
        pb_tags = t.get_prev_block_tags()
        nb_tags = t.get_next_block_tags(number_of_blocks=3)
        if da_phrase_si := search_da_phrase(pb_tags + nb_tags):
            sem_roles.append(
                AteSemRole(
                    " ".join(x.occ for x in da_phrase_si), [verb, v], "ACTIVE", [v],
                )
            )
    elif t.is_middle_pr():
        sem_roles.append(
            AteSemRole(" ".join(x.occ for x in sogg), [verb, v], "PASSIVE", [v])
        )
    elif t.is_past_participle():
        v_block = [x for x in t.get_same_block_tags() if x.index < t.index]
        sem_roles.append(
            AteSemRole(" ".join(x.occ for x in v_block), [verb, v], "PASSIVE", [v])
        )
