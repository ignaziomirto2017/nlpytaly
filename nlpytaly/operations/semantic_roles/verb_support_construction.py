from typing import List

from ...data.verb_support import data
from ...data.verbs.class_1_verbs import two_place_predicate1
from ...data.verbs.intransitives import all_intransitives, class_1_verbs
from ...data.verbs.trivalent import trivalent_verbs
from ...operations.semantic_roles.SemRole.SemRole import SuppSemRole
from ...Tag import Tag
from ...Utils import (
    get_subj_obj_tags_for_tag,
    mark_tag,
    search_a_phrase,
    search_da_phrase,
)
from .pred_assigners import pred_sem_fare_caus, pred_sem_supp, pred_syn_supp
from .SemRole.SemRole import DativeSemRole
from .utils import assign_and_increment


def mark_verb_support_construction(tags: List[Tag]):
    exclusions: List[int] = []
    for t in tags:
        # -----------------------------------
        # Es. "Mario fa allusione al tuo caso"
        # evita che l'esito sia quello di 'fare caso'
        p1, p2 = t.prev(), t.prev(step=2)
        p1pos = p1.pos if p1 else ""
        p2pos = p2.pos if p2 else ""

        if "PRE" in p1pos or "PRE" in p2pos:
            continue
        # -----------------------------------

        if t.lemma in data:
            for p in t.get_prev_block_tags(
                step=2, number_of_blocks=2
            ) + t.get_next_block_tags(number_of_blocks=2):
                if p.lemma in data[t.lemma]["verbi_supp"]:
                    mark_tag(p, pred_syn_supp, t)  # fare
                    mark_tag(t, pred_sem_supp, p)  # sorriso
                    if p.is_active():
                        exclusions.append(t.index)
                    verb = data[t.lemma]["verbo"]
                    if verb in class_1_verbs:
                        p.set_max_assignable_sem_roles(1)
                    elif verb in two_place_predicate1:
                        p.set_max_assignable_sem_roles(2)
                    elif verb in trivalent_verbs:
                        p.set_max_assignable_sem_roles(3)
                    else:
                        p.set_max_assignable_sem_roles(2)
        else:
            pass
    return exclusions


def assign_verb_support_construction(t: Tag, v, syntactic_roles, tags, sem_roles):
    is_fare_caus = any(hasattr(x, pred_sem_fare_caus) for x in t.get_same_block_tags())
    verbo_supp_tag: Tag = t
    sostantivo_tag = v
    cognate_verb = data[sostantivo_tag.lemma]["verbo"]
    diathesis = data[sostantivo_tag.lemma].get("diathesis", None) or "ACTIVE"
    additional_f2 = data[sostantivo_tag.lemma].get("f2", [])
    worded = data[sostantivo_tag.lemma].get("worded", False)

    f2 = [cognate_verb]
    f2.extend(additional_f2)

    neg = t.is_negative_inflected_verb()

    subj, _, _, _ = get_subj_obj_tags_for_tag(verbo_supp_tag, tags, syntactic_roles)
    subj: List[Tag]
    if subj:
        pass
    elif subj is None and t.cov_sub:
        subj = [Tag(t.cov_sub, "-", "-")]
    else:
        subj = []
    if verbo_supp_tag.is_active() and not verbo_supp_tag.is_aux():
        if not is_fare_caus:
            assign_and_increment(
                verbo_supp_tag,
                SuppSemRole(" ".join(x.occ for x in subj), f2, diathesis, worded, neg),
                sem_roles,
            )
        if a_phrase_si := search_a_phrase(
            t.get_next_block_tags(number_of_blocks=2) + t.get_prev_block_tags()
        ):
            if not is_fare_caus:
                if cognate_verb in all_intransitives or cognate_verb in trivalent_verbs:
                    assign_and_increment(
                        verbo_supp_tag,
                        DativeSemRole(" ".join(x.occ for x in a_phrase_si), f2),
                        sem_roles,
                    )
                else:
                    assign_and_increment(
                        verbo_supp_tag,
                        SuppSemRole(
                            " ".join(x.occ for x in a_phrase_si),
                            f2,
                            "PASSIVE",
                            worded,
                            neg,
                        ),
                        sem_roles,
                    )
    elif verbo_supp_tag.is_passive() and not verbo_supp_tag.is_aux():
        if a_phrase_si := search_a_phrase(
            t.get_next_block_tags(number_of_blocks=2) + t.get_prev_block_tags()
        ):
            if not is_fare_caus:
                if cognate_verb in all_intransitives or cognate_verb in trivalent_verbs:
                    assign_and_increment(
                        verbo_supp_tag,
                        DativeSemRole(" ".join(x.occ for x in a_phrase_si), f2, neg),
                        sem_roles,
                    )
                else:
                    assign_and_increment(
                        verbo_supp_tag,
                        SuppSemRole(
                            " ".join(x.occ for x in a_phrase_si),
                            f2,
                            "PASSIVE",
                            worded,
                            neg,
                        ),
                        sem_roles,
                    )

        if da_phrase_si := search_da_phrase(
            t.get_next_block_tags(number_of_blocks=2) + t.get_prev_block_tags()
        ):
            if not is_fare_caus:
                assign_and_increment(
                    verbo_supp_tag,
                    SuppSemRole(
                        " ".join(x.occ for x in da_phrase_si), f2, "ACTIVE", worded, neg
                    ),
                    sem_roles,
                )
    elif verbo_supp_tag.is_middle():
        # si fece un sorriso ai presenti
        # Luigi si fece un sorriso
        if verbo_supp_tag.is_middle_pr():
            # Luigi si fece un sorriso ..
            assign_and_increment(
                verbo_supp_tag,
                SuppSemRole(" ".join(x.occ for x in subj), f2, diathesis, worded, neg),
                sem_roles,
            )
        else:
            # mr
            # impersonale, Si fece un sorriso ai presenti
            pass
