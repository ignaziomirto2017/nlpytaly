from typing import List

from .SemRole import DativeSemRole, OrdinarySemRole
from .pred_assigners import pred_sem_supp, pred_syn_supp, pred_sem_fare_caus
from ...Tag import Tag
from ...Utils import get_subj_obj_tags_for_tag, mark_tag, search_a_phrase
from ...data.verb_support import data
from ...data.verbs.intransitives import all_intransitives
from ...operations.semantic_roles.SemRole import SuppSemRole


def mark_verb_support_construction(tags: List[Tag]):
    for t in tags:
        if t.lemma in data:
            for p in t.get_prev_block_tags():
                if p.lemma in data[t.lemma]["verbi_supp"]:
                    mark_tag(p, pred_syn_supp, t)
                    mark_tag(t, pred_sem_supp, p)


def assign_verb_support_construction(
    t, v, syntactic_roles, tags, sem_roles, sem_roles_cov_subjects: dict,
):
    is_fare_caus = any(hasattr(x, pred_sem_fare_caus) for x in t.get_same_block_tags())
    verbo_supp_tag: Tag = t
    sostantivo_tag = v
    cognate_verb = data[sostantivo_tag.lemma]["verbo"]
    diathesis = data[sostantivo_tag.lemma].get("diathesis", None) or "ACTIVE"

    subj, _, _, _ = get_subj_obj_tags_for_tag(verbo_supp_tag, tags, syntactic_roles)
    subj: List[Tag]
    if verbo_supp_tag.is_active() and not verbo_supp_tag.is_aux():
        if subj:
            if subj[0].sem_role_allowed(verbo_supp_tag.get_same_block_indexes()):
                sem_roles.append(
                    SuppSemRole(
                        " ".join(x.occ for x in subj), [cognate_verb], diathesis,
                    )
                )

        else:
            if not (t.cov_sub, cognate_verb) in sem_roles_cov_subjects:
                sem_roles.append(OrdinarySemRole(t.cov_sub, [cognate_verb], "ACTIVE"))
                sem_roles_cov_subjects[(t.cov_sub, cognate_verb)] = True

        if a_phrase_si := search_a_phrase(
            t.get_next_block_tags(number_of_blocks=2) + t.get_prev_block_tags()
        ):
            if not is_fare_caus:
                if cognate_verb in all_intransitives:
                    sem_roles.append(
                        DativeSemRole(
                            " ".join(x.occ for x in a_phrase_si), [cognate_verb]
                        )
                    )
                else:
                    sem_roles.append(
                        SuppSemRole(
                            " ".join(x.occ for x in a_phrase_si),
                            [cognate_verb],
                            "PASSIVE",
                        )
                    )
