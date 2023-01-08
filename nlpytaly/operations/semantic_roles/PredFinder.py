from typing import List

from ...data.verbs.bivalent import v12, v12_2si
from ...data.verbs.class_2_verbs import class_2_verbs_si, two_place_predicate2
from ...data.verbs.intransitives import all_intransitives, all_intransitives__no_weather
from ...data.verbs.trivalent import trivalent_verbs
from ...data.verbs.weather_verbs import weather_verbs
from ...Tag import Tag
from ...Utils import (
    get_attr,
    get_subj_obj_tags_for_tag,
    mark_tag,
    search_a_phrase,
    search_da_phrase,
)
from .ate_suffix_construction import assign_ate_suffix, mark_ate_suffix
from .causative_fare_construction import assign_causative_fare
from .from_adjectival_pp import assign_adj_past_part, mark_adj_past_part
from .job_fare_construction import assign_job_sem_role
from .mettere_prep_construction import (
    assign_mettere_prep,
    assign_mettere_prep_ov,
    mark_mettere_prep,
)
from .pred_assigners import (
    pred_sem_fare_caus,
    pred_sem_ord,
    pred_sem_pper,
    pred_syn_ate,
    pred_syn_mest,
    pred_syn_mettere_prep,
    pred_syn_mettere_prep_ov,
    pred_syn_supp,
)
from .SemRole.consts import ACTV, ACTV_S, PASSV
from .SemRole.SemRole import (
    AbstractSemRole,
    AmbiguousSemRole,
    CausativeSemRole,
    DativeSemRole,
    OrdinarySemRole,
)
from .utils import assign_and_increment
from .verb_support_construction import assign_verb_support_construction


def _handle_special_ord_verb(od, sem_roles, sogg, t):
    occ = t.get_same_block_occurrences()
    if t.lemma == "volere":
        if "bene" == t.get_same_block_occurrences()[-1]:
            return "amare"
        if "ci" in occ:
            return "servire"
    return t.lemma


def number_of(sub, od):
    if sub and od:
        return 2
    if sub and not od:
        return 1
    if not sub and not od:
        return 0


def assign_ord_verb(
    od, sem_roles, subj, t: Tag, candidates_indexes: List[List[List[int]]], amb
):
    is_causative_fare = any(
        hasattr(x, pred_sem_fare_caus) for x in t.get_same_block_tags()
    )
    adv = []
    prev = t.prev()
    next = t.next()
    if prev and prev.is_adverb() and prev.lemma.endswith("mente"):
        adv = [prev.lemma]
    elif next and next.is_adverb() and next.lemma.endswith("mente"):
        adv = [next.lemma]
    verb = _handle_special_ord_verb(od, sem_roles, subj, t)

    # Overt or covert subject
    subj = [Tag(t.cov_sub, "-", "-")] if not subj else subj

    # Enclitc object or direct object (or None)
    od = [Tag(t.encl_od, "-", "-")] if (not od and t.encl_od) else od

    f2 = [verb]
    f2.extend(adv)

    neg = t.is_negative_inflected_verb()

    if is_dativo_clit := [x for x in t.get_same_block_tags() if x.note == "OGG INDIR"]:
        if not is_causative_fare and t.can_assign_sem_roles():
            if verb in v12:
                assign_and_increment(
                    t,
                    OrdinarySemRole(
                        " ".join(x.occ for x in is_dativo_clit), f2, PASSV, neg
                    ),
                    sem_roles,
                )
            else:
                assign_and_increment(
                    t,
                    DativeSemRole(" ".join(x.occ for x in is_dativo_clit), [verb], neg),
                    sem_roles,
                )

    if t.is_active():
        if od:
            if verb in all_intransitives and is_causative_fare:
                assign_and_increment(
                    t,
                    OrdinarySemRole(" ".join(x.occ for x in od), f2, ACTV, neg),
                    sem_roles,
                )
            elif verb in v12_2si:
                assign_and_increment(
                    t,
                    OrdinarySemRole(" ".join(x.occ for x in od), f2, ACTV_S, neg),
                    sem_roles,
                )
            elif verb in v12:
                assign_and_increment(
                    t,
                    OrdinarySemRole(" ".join(x.occ for x in od), f2, PASSV, neg),
                    sem_roles,
                )
            else:
                assign_and_increment(
                    t,
                    OrdinarySemRole(" ".join(x.occ for x in od), f2, PASSV, neg),
                    sem_roles,
                )
        if not is_causative_fare:
            if verb in weather_verbs:
                pass
            else:
                if amb is None:
                    if verb in v12:
                        if number_of(subj, od) == 2:
                            assign_and_increment(
                                t,
                                CausativeSemRole(
                                    " ".join(x.occ for x in subj),
                                    ["fare"],
                                    "ACTIVE",
                                    verb,
                                    neg,
                                ),
                                sem_roles,
                            )
                        elif number_of(subj, od) == 1:
                            assign_and_increment(
                                t,
                                OrdinarySemRole(
                                    " ".join(x.occ for x in subj), f2, PASSV, neg
                                ),
                                sem_roles,
                            )
                    else:
                        assign_and_increment(
                            t,
                            OrdinarySemRole(
                                " ".join(x.occ for x in subj), f2, ACTV, neg
                            ),
                            sem_roles,
                        )
                else:
                    assign_and_increment(
                        t,
                        AmbiguousSemRole(
                            f1=" ".join(x.occ for x in amb),
                            f2=f2,
                            role1=OrdinarySemRole(
                                " ".join(x.occ for x in amb), f2, ACTV, neg
                            ),
                            role2=OrdinarySemRole(
                                " ".join(x.occ for x in amb), f2, PASSV, neg
                            ),
                        ),
                        sem_roles,
                    )
        if a_phrase_si := search_a_phrase(t.get_next_block_tags(number_of_blocks=2)):
            if not is_causative_fare and t.can_assign_sem_roles():
                if verb in v12:
                    assign_and_increment(
                        t,
                        OrdinarySemRole(
                            " ".join(x.occ for x in a_phrase_si), f2, PASSV, neg
                        ),
                        sem_roles,
                    )
                else:
                    assign_and_increment(
                        t,
                        DativeSemRole(
                            " ".join(x.occ for x in a_phrase_si), [verb], neg
                        ),
                        sem_roles,
                    )
    elif t.is_passive():
        if subj and t.can_assign_sem_roles():
            if verb in weather_verbs:
                pass
            elif verb in all_intransitives__no_weather:
                assign_and_increment(
                    t,
                    OrdinarySemRole(" ".join(x.occ for x in subj), f2, ACTV, neg),
                    sem_roles,
                )
            else:
                assign_and_increment(
                    t,
                    OrdinarySemRole(" ".join(x.occ for x in subj), f2, PASSV, neg),
                    sem_roles,
                )
        pb_tags = t.get_prev_block_tags()
        nb_tags = t.get_next_block_tags(number_of_blocks=2)
        if (
            (da_phrase_si := search_da_phrase(pb_tags + nb_tags))
            and not is_causative_fare
            and t.can_assign_sem_roles()
        ):
            assign_and_increment(
                t,
                OrdinarySemRole(" ".join(x.occ for x in da_phrase_si), f2, ACTV, neg),
                sem_roles,
            )

        if a_phrase_si := search_a_phrase(
            t.get_next_block_tags(number_of_blocks=2) + t.get_prev_block_tags()
        ):
            if not is_causative_fare:
                if verb in v12:
                    pass
                else:
                    assign_and_increment(
                        t,
                        DativeSemRole(
                            " ".join(x.occ for x in a_phrase_si), [verb], neg
                        ),
                        sem_roles,
                    )
    elif t.is_middle_mr():
        if a_phrase_si := search_a_phrase(t.get_next_block_tags(number_of_blocks=2)):
            if not is_causative_fare:
                if verb in two_place_predicate2:
                    assign_and_increment(
                        t,
                        DativeSemRole(
                            " ".join(x.occ for x in a_phrase_si), [verb], neg
                        ),
                        sem_roles,
                    )
        if subj:
            if verb in class_2_verbs_si | v12_2si:
                assign_and_increment(
                    t,
                    OrdinarySemRole(" ".join(x.occ for x in subj), f2, ACTV_S, neg),
                    sem_roles,
                )
            else:
                assign_and_increment(
                    t,
                    OrdinarySemRole(" ".join(x.occ for x in subj), f2, ACTV, neg),
                    sem_roles,
                )
        else:
            pass
    elif t.is_middle_pr():
        if subj:
            if t.lemma not in all_intransitives:
                if (
                    subj[0].index < t.index
                ):  # se il sogg. è preverbale es. I bambini si lavano
                    if not is_causative_fare:
                        assign_and_increment(
                            t,
                            OrdinarySemRole(
                                " ".join(x.occ for x in subj), f2, ACTV, neg
                            ),
                            sem_roles,
                        )
                if not is_causative_fare:
                    if (
                        verb in trivalent_verbs
                        and len(t.get_adjacent_candidates(candidates_indexes)) == 2
                    ):
                        assign_and_increment(
                            t,
                            DativeSemRole(" ".join(x.occ for x in subj), [verb], neg),
                            sem_roles,
                        )
                    else:
                        assign_and_increment(
                            t,
                            OrdinarySemRole(
                                " ".join(x.occ for x in subj), f2, PASSV, neg
                            ),
                            sem_roles,
                        )
            else:  # intransitives
                assign_and_increment(
                    t,
                    OrdinarySemRole(" ".join(x.occ for x in subj), f2, PASSV, neg),
                    sem_roles,
                )
        else:  # no subj found
            pass
        if od:
            assign_and_increment(
                t,
                OrdinarySemRole(" ".join(x.occ for x in od), f2, PASSV, neg),
                sem_roles,
            )


def pred_finder(
    tags: List[Tag],
    sem_roles: List[AbstractSemRole],
    syntactic_roles: dict,
    candidates_indexes: List[List[List[int]]],
):
    for t in tags:
        sogg, od, _, amb = get_subj_obj_tags_for_tag(t, tags, syntactic_roles)
        sogg: List[Tag]
        od: List[Tag]
        if v := get_attr(t, pred_sem_fare_caus):
            assign_causative_fare(sem_roles, sogg, t, v, amb)
        elif v := get_attr(t, pred_syn_mest):
            assign_job_sem_role(sem_roles, sogg, t, v)
        elif v := get_attr(t, pred_syn_mettere_prep):
            assign_mettere_prep(od, sem_roles, sogg, t, v, amb)
        elif data := get_attr(t, pred_syn_mettere_prep_ov):
            assign_mettere_prep_ov(sem_roles, t, data)
        elif v := get_attr(t, pred_syn_ate):
            assign_ate_suffix(od, sem_roles, sogg, t, v, amb)
        elif v := get_attr(t, pred_sem_pper):
            assign_adj_past_part(od, sem_roles, sogg, t, v)
        elif v := get_attr(t, pred_syn_supp):
            assign_verb_support_construction(t, v, syntactic_roles, tags, sem_roles)
        elif v := get_attr(t, pred_sem_ord):
            assign_ord_verb(od, sem_roles, sogg, t, candidates_indexes, amb)


def mark(tags: List[Tag], prep_inf: List[List[int]]) -> None:
    mark_mettere_prep(tags)
    # moved to nlpytaly.py
    # mark_verb_support_construction(tags)
    mark_ate_suffix(tags)
    # moved to nlpytaly.py
    # fare_causativo_mark(tags)
    mark_adj_past_part(tags)

    for t in tags:
        if not t.is_marked() and (
            (not t.is_aux() and t.is_in_SV_block() and t.is_verb()) or t.is_gerund()
        ):
            mark_tag(t, pred_sem_ord, t)

    for group in prep_inf:
        for index in group:
            t = tags[index]
            if t.is_infinitive():
                mark_tag(tags[index], pred_sem_ord, tags[index])

    print("\nPREDs")
    for t in tags:
        for s in dir(t):
            if s.startswith("PRED"):
                print("\t", t, s)
