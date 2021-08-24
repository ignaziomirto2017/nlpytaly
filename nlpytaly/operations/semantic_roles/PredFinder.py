from typing import List

from .SemRole.SemRole import (
    AbstractSemRole,
    OrdinarySemRole,
    DativeSemRole,
)
from .ate_suffix_construction import mark_ate_suffix, assign_ate_suffix
from .causative_fare_construction import assign_causative_fare
from .from_adjectival_pp import mark_adj_past_part, assign_adj_past_part
from .job_fare_construction import assign_job_sem_role
from .mettere_prep_construction import mark_mettere_prep, assign_mettere_prep
from .pred_assigners import *
from .verb_support_construction import (
    mark_verb_support_construction,
    assign_verb_support_construction,
)
from ...Tag import Tag
from ...Utils import (
    get_subj_obj_tags_for_tag,
    get_attr,
    mark_tag,
    search_da_phrase,
    search_a_phrase,
)
from ...data.verbs.bivalent import v12, v12_2si
from ...data.verbs.class_2_verbs import class_2_verbs_si
from ...data.verbs.intransitives import all_intransitives, all_intransitives__no_weather
from ...data.verbs.trivalent import trivalent_verbs
from ...data.verbs.weather_verbs import weather_verbs


def pred_finder(
    tags: List[Tag],
    sem_roles: List[AbstractSemRole],
    syntactic_roles: dict,
    sem_roles_cov_subjects: dict,
    candidates_indexes: List[List[List[int]]],
):
    for t in tags:
        sogg, od, _, _ = get_subj_obj_tags_for_tag(t, tags, syntactic_roles)
        sogg: List[Tag]
        od: List[Tag]
        if v := get_attr(t, pred_sem_fare_caus):
            assign_causative_fare(sem_roles, sogg, t, v, sem_roles_cov_subjects)
        elif v := get_attr(t, pred_sem_ord):
            assign_ord_verb(
                od, sem_roles, sogg, t, sem_roles_cov_subjects, candidates_indexes
            )
        elif v := get_attr(t, pred_syn_mest):
            assign_job_sem_role(sem_roles, sogg, t, v)
        elif v := get_attr(t, pred_syn_mettere_prep):
            assign_mettere_prep(od, sem_roles, sogg, t, v)
        elif v := get_attr(t, pred_syn_ate):
            assign_ate_suffix(od, sem_roles, sogg, t, v)
        elif v := get_attr(t, pred_sem_pper):
            assign_adj_past_part(od, sem_roles, sogg, t, v)
        elif v := get_attr(t, pred_syn_supp):
            assign_verb_support_construction(
                t, v, syntactic_roles, tags, sem_roles, sem_roles_cov_subjects
            )


def _handle_special_ord_verb(od, sem_roles, sogg, t):
    occ = t.get_same_block_occurrences()
    if t.lemma == "volere":
        if "bene" == t.get_same_block_occurrences()[-1]:
            return "amare"
        if "ci" in occ:
            return "servire"
    return t.lemma


def assign_ord_verb(
    od,
    sem_roles,
    subj,
    t: Tag,
    sem_roles_cov_subjects: dict,
    candidates_indexes: List[List[List[int]]],
):
    is_causative_fare = any(
        hasattr(x, pred_sem_fare_caus) for x in t.get_same_block_tags()
    )
    verb = _handle_special_ord_verb(od, sem_roles, subj, t)
    if t.is_active():
        if subj:
            if subj and subj[0].sem_role_allowed(t.get_same_block_indexes()):
                for s in subj:
                    s.sem_role_inc(t.get_same_block_indexes())
                sem_roles.append(
                    OrdinarySemRole(" ".join(x.occ for x in subj), [verb], "ACTIVE")
                )
        else:
            if not (t.cov_sub, verb) in sem_roles_cov_subjects:
                sem_roles.append(OrdinarySemRole(t.cov_sub, [verb], "ACTIVE"))
                sem_roles_cov_subjects[(t.cov_sub, verb)] = True
        if od and od[0].sem_role_allowed(t.get_same_block_indexes()):
            for o in od:
                o.sem_role_inc(t.get_same_block_indexes())
            if verb in all_intransitives:
                sem_roles.append(
                    OrdinarySemRole(" ".join(x.occ for x in od), [verb], "ACTIVE")
                )
            elif verb in v12_2si:
                sem_roles.append(
                    OrdinarySemRole(" ".join(x.occ for x in od), [verb], "ACTIVE_SI")
                )
            elif verb in v12:
                sem_roles.append(
                    OrdinarySemRole(" ".join(x.occ for x in od), [verb], "PASSIVE")
                )
                sem_roles.append(
                    OrdinarySemRole(" ".join(x.occ for x in od), [verb], "ACTIVE")
                )

            else:
                sem_roles.append(
                    OrdinarySemRole(" ".join(x.occ for x in od), [verb], "PASSIVE")
                )
        if a_phrase_si := search_a_phrase(t.get_next_block_tags(number_of_blocks=2)):
            if not is_causative_fare:
                if verb in v12:
                    sem_roles.append(
                        OrdinarySemRole(
                            " ".join(x.occ for x in a_phrase_si), [verb], "PASSIVE"
                        )
                    )
                else:
                    sem_roles.append(
                        DativeSemRole(" ".join(x.occ for x in a_phrase_si), [verb])
                    )
    elif t.is_passive():
        if subj and subj[0].sem_role_allowed(t.get_same_block_indexes()):
            for s in subj:
                s.sem_role_inc(t.get_same_block_indexes())
            if verb in weather_verbs:
                pass
            elif verb in all_intransitives__no_weather:
                sem_roles.append(
                    OrdinarySemRole(" ".join(x.occ for x in subj), [verb], "ACTIVE")
                )
            else:
                sem_roles.append(
                    OrdinarySemRole(" ".join(x.occ for x in subj), [verb], "PASSIVE")
                )
        pb_tags = t.get_prev_block_tags()
        nb_tags = t.get_next_block_tags(number_of_blocks=2)
        if (
            da_phrase_si := search_da_phrase(pb_tags + nb_tags)
        ) and not is_causative_fare:
            sem_roles.append(
                OrdinarySemRole(
                    " ".join(x.occ for x in da_phrase_si), [verb], "ACTIVE",
                )
            )
        if a_phrase_si := search_a_phrase(
            t.get_next_block_tags(number_of_blocks=2) + t.get_prev_block_tags()
        ):
            if not is_causative_fare:
                if verb in v12:
                    pass
                else:
                    sem_roles.append(
                        DativeSemRole(" ".join(x.occ for x in a_phrase_si), [verb])
                    )
    elif t.is_middle_mr():
        if subj and subj[0].sem_role_allowed(t.get_same_block_indexes()):
            for s in subj:
                s.sem_role_inc(t.get_same_block_indexes())
            if verb in class_2_verbs_si | v12_2si:
                sem_roles.append(
                    OrdinarySemRole(" ".join(x.occ for x in subj), [verb], "ACTIVE_SI")
                )
            else:
                sem_roles.append(
                    OrdinarySemRole(" ".join(x.occ for x in subj), [verb], "ACTIVE")
                )
        else:
            if not (t.cov_sub, verb) in sem_roles_cov_subjects:
                sem_roles.append(OrdinarySemRole(t.cov_sub, [verb], "ACTIVE"))
                sem_roles_cov_subjects[(t.cov_sub, verb)] = True
    elif t.is_middle_pr():
        if subj and subj[0].sem_role_allowed(t.get_same_block_indexes()):
            for s in subj:
                s.sem_role_inc(t.get_same_block_indexes())
            if t.lemma not in all_intransitives:
                if (
                    subj[0].index < t.index
                ):  # se il sogg. è preverbale es. I bambini si lavano
                    if not is_causative_fare:
                        sem_roles.append(
                            OrdinarySemRole(
                                " ".join(x.occ for x in subj), [verb], "ACTIVE"
                            )
                        )
                if not is_causative_fare:
                    if (
                        verb in trivalent_verbs
                        and len(t.get_adjacent_candidates(candidates_indexes)) == 2
                    ):
                        sem_roles.append(
                            DativeSemRole(" ".join(x.occ for x in subj), [verb])
                        )
                    else:
                        sem_roles.append(
                            OrdinarySemRole(
                                " ".join(x.occ for x in subj), [verb], "PASSIVE"
                            )
                        )
            else:  # intransitives
                sem_roles.append(
                    OrdinarySemRole(" ".join(x.occ for x in subj), [verb], "PASSIVE")
                )
        else:  # no subj found
            if not (t.cov_sub, verb) in sem_roles_cov_subjects:
                sem_roles.append(OrdinarySemRole(t.cov_sub, [verb], "ACTIVE"))
                sem_roles_cov_subjects[(t.cov_sub, verb)] = True
        if od and od[0].sem_role_allowed(t.get_same_block_indexes()):
            for o in od:
                o.sem_role_inc(t.get_same_block_indexes())
            sem_roles.append(
                OrdinarySemRole(" ".join(x.occ for x in od), [verb], "PASSIVE")
            )

    # TODO: Antonio si lamenta con Giovanni


def mark(tags: List[Tag], prep_inf: List[List[int]]) -> None:
    # attenzione a Il tenente ha fatto mettere sotto accusa il sottoposto
    # fare_mest già fatto in nlpytaly per esclusioni OD

    mark_mettere_prep(tags)
    mark_verb_support_construction(tags)
    mark_ate_suffix(tags)
    # moved to nlpytaly.py
    # fare_causativo_mark(tags)
    mark_adj_past_part(tags)

    for t in tags:
        if (
            not t.is_aux() and t.is_in_SV_block() and not t.is_marked() and t.is_verb()
        ) or t.is_gerund():
            mark_tag(t, pred_sem_ord, t)

    for group in prep_inf:
        for index in group:
            t = tags[index]
            if t.is_infinitive():
                mark_tag(tags[index], pred_sem_ord, tags[index])

    print("PREDs")
    for t in tags:
        for s in dir(t):
            if s.startswith("PRED"):
                print(t, s)
