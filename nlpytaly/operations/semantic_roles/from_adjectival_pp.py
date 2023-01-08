from typing import List

from nlpytaly.operations.semantic_roles.utils import assign_and_increment

from ...data.verbs.intransitives import all_intransitives
from ...data.verbs.intransitives import class_2_verbs as intr_class2
from ...Tag import Tag
from ...Utils import mark_tag, search_da_phrase
from .pred_assigners import pred_sem_pper
from .SemRole.SemRole import OrdinarySemRole


def mark_adj_past_part(tags: List[Tag]):
    for t in tags:
        if t.is_past_participle() and t.is_in_SN_block() and not t.is_marked():
            if not any(
                x.is_noun()
                for x in (y for y in t.get_same_block_tags() if y.index < t.index)
            ):
                break
            mark_tag(
                t,
                pred_sem_pper,
                [
                    x
                    for x in tags
                    if x.index < t.index and x.block == t.block
                    # E' necessario? O basta la parte x.index < t.index and x.block == t.block
                    and (x.is_article() or x.is_adjective() or x.is_noun())
                ],
            )
            if t.lemma in all_intransitives:
                t.set_max_assignable_sem_roles(1)
            else:
                t.set_max_assignable_sem_roles(2)


def assign_adj_past_part(od, sem_roles, sogg, t: Tag, v):
    verb = t.lemma
    if verb in intr_class2:
        mode = "ACTIVE"
    else:
        mode = "PASSIVE"
    if t.can_assign_sem_roles():
        assign_and_increment(
            t, OrdinarySemRole(" ".join(x.occ for x in v), [t.lemma], mode), sem_roles
        )
    if mode == "PASSIVE":
        if da_phrase_si := search_da_phrase(t.get_next_block_tags()):
            if t.can_assign_sem_roles():
                assign_and_increment(
                    t,
                    OrdinarySemRole(
                        " ".join(x.occ for x in da_phrase_si), [verb], "ACTIVE"
                    ),
                    sem_roles,
                )
