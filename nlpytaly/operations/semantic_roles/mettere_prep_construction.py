from typing import List

from .SemRole.SemRole import MetterePrepSemRole
from .pred_assigners import *
from ...Tag import Tag
from ...Utils import (
    mark_tag,
    search_da_phrase,
)
from ...data.mettere_prep import mettere_prep_dict


def mark_mettere_prep(tags: List[Tag],):
    for t in tags:
        if t.lemma in mettere_prep_dict:
            # t.lemma = sotto, a, ...
            p_tags = t.get_prev_block_tags(step=2, number_of_blocks=2)
            s_tags = [tmp for tmp in t.get_same_block_tags() if tmp.index > t.index]

            for t_noun in s_tags:
                if t_noun.occ in mettere_prep_dict[t.lemma]:
                    break
            else:
                continue

            for v in p_tags:
                if v.lemma == "mettere":
                    mark_tag(
                        v,
                        pred_syn_mettere_prep,
                        (mettere_prep_dict[t.lemma][t_noun.occ]["v"], (t, t_noun)),
                    )
                    mark_tag(t_noun, pred_sem_mettere_prep, v)
                    # increment_blocks(tags, t.index, t_noun.index)


def assign_mettere_prep(od, sem_roles, sogg, t, v):
    is_fare_caus = any(hasattr(x, pred_sem_fare_caus) for x in t.get_same_block_tags())
    v, noun = v[0], v[1]
    if t.is_active():
        if sogg and sogg[0].sem_role_allowed(t.get_same_block_indexes()):
            sem_roles.append(
                MetterePrepSemRole(" ".join(x.occ for x in sogg), [v], "ACTIVE", noun)
            )

        if od and od[0].sem_role_allowed(t.get_same_block_indexes()):
            sem_roles.append(
                MetterePrepSemRole(" ".join(x.occ for x in od), [v], "PASSIVE", noun)
            )

        if is_fare_caus:
            if da_phrase_si := search_da_phrase(
                t.get_next_block_tags(number_of_blocks=4)
            ):
                sem_roles.append(
                    MetterePrepSemRole(
                        " ".join(x.occ for x in da_phrase_si), [v], "ACTIVE", noun
                    )
                )
    elif t.is_passive():
        if sogg and sogg[0].sem_role_allowed(t.get_same_block_indexes()):
            sem_roles.append(
                MetterePrepSemRole(" ".join(x.occ for x in sogg), [v], "PASSIVE", noun)
            )
        if da_phrase_si := search_da_phrase(t.get_next_block_tags(number_of_blocks=2)):
            sem_roles.append(
                MetterePrepSemRole(
                    " ".join(x.occ for x in da_phrase_si), [v], "ACTIVE", noun
                )
            )
    # TODO: middle_pr
