from typing import List

from .SemRole.SemRole import OrdinarySemRole
from .pred_assigners import *
from ...Tag import Tag
from ...Utils import mark_tag, search_da_phrase
from ...data.verbs.intransitives import class_2_verbs as intr_class2


def mark_adj_past_part(tags: List[Tag],):
    for t in tags:
        if t.is_past_participle() and t.is_in_SN_block() and not t.is_marked():
            mark_tag(
                t,
                pred_sem_pper,
                [
                    x
                    for x in tags
                    if x.index < t.index
                    and x.block == t.block
                    and (x.is_article(), x.is_noun())
                ],
            )


def assign_adj_past_part(od, sem_roles, sogg, t: Tag, v):
    verb = t.lemma
    if verb in intr_class2:
        mode = "ACTIVE"
    else:
        mode = "PASSIVE"
    sem_roles.append(OrdinarySemRole(" ".join(x.occ for x in v), [t.lemma], mode))
    if mode == "PASSIVE":
        if da_phrase_si := search_da_phrase(t.get_next_block_tags()):
            sem_roles.append(
                OrdinarySemRole(
                    " ".join(x.occ for x in da_phrase_si), [verb], "ACTIVE",
                )
            )
