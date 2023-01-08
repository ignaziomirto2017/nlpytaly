from typing import List

from ...data.ate_multiwords import (
    ate_multiwords,
    ate_multiwords_colpire,
    ate_multiwords_insultare,
)
from ...data.verb_support import data
from ...data.verbs.intransitives import all_intransitives
from ...data.verbs.trivalent import trivalent_verbs
from ...Tag import Tag
from ...Utils import mark_tag, search_a_phrase, search_da_phrase
from .pred_assigners import pred_sem_fare_caus, pred_syn_supp
from .SemRole.SemRole import (
    AteSemRole,
    CausativeSemRole,
    DativeSemRole,
    JobSemRole,
    OrdinarySemRole,
    SuppSemRole,
)
from .utils import assign_and_increment


def mark_causative_fare(tags: List[Tag]):
    for t in tags:
        if t.lemma == "fare" or t.lemma == "lasciare":
            if is_causative_fare := [
                x
                for x in t.get_same_block_tags()
                if "infi" in x.pos and t.index < x.index
            ]:
                t.is_causative_fare = True
                mark_tag(t, pred_sem_fare_caus, is_causative_fare[0])
                t.set_max_assignable_sem_roles(1)


def assign_causative_fare(sem_roles, sogg, t: Tag, v: Tag, amb: List[Tag]):
    sogg = [Tag(t.cov_sub, "-", "-")] if (not sogg) else sogg
    if t.is_active():
        if hasattr(t, pred_sem_fare_caus):
            if (
                any(x.startswith("PRED_SEM") for x in dir(v))
                and t.can_assign_sem_roles()
            ):
                assign_and_increment(
                    t,
                    CausativeSemRole(
                        " ".join(x.occ for x in sogg), ["fare"], "ACTIVE", v.occ
                    ),
                    sem_roles,
                )
            else:
                if hasattr(v, "PRED_SYN_ATE"):
                    verb = getattr(v, "PRED_SYN_ATE")
                    f3 = None
                    if verb in ate_multiwords:
                        f3 = ate_multiwords[verb]
                    elif verb in ate_multiwords_colpire:
                        f3 = "colpire"
                    elif verb in ate_multiwords_insultare:
                        f3 = "insultare"
                    if f3:
                        assign_and_increment(
                            t,
                            CausativeSemRole(
                                " ".join(x.occ for x in sogg), ["fare"], "ACTIVE", f3
                            ),
                            sem_roles,
                        )
                elif hasattr(v, "PRED_SYN_MEST"):
                    mestiere = getattr(v, "PRED_SYN_MEST").lemma
                    assign_and_increment(
                        t,
                        CausativeSemRole(
                            " ".join(x.occ for x in sogg),
                            ["fare"],
                            "ACTIVE",
                            "LAVORARE",
                        ),
                        sem_roles,
                    )
                    if a_phrase_si := search_a_phrase(
                        t.get_next_block_tags(number_of_blocks=2)
                        + t.get_prev_block_tags(number_of_blocks=2)
                    ):
                        assign_and_increment(
                            v,
                            JobSemRole(" ".join(x.occ for x in a_phrase_si), mestiere),
                            sem_roles,
                        )
                if hasattr(v, "PRED_SYN_METTERE_PREP"):
                    if not amb:
                        assign_and_increment(
                            t,
                            CausativeSemRole(
                                " ".join(x.occ for x in sogg),
                                ["fare"],
                                "ACTIVE",
                                getattr(v, "PRED_SYN_METTERE_PREP")[0],
                            ),
                            sem_roles,
                        )
                    else:
                        assign_and_increment(
                            t,
                            CausativeSemRole(
                                "LUI|LEI",
                                ["fare"],
                                "ACTIVE",
                                getattr(v, "PRED_SYN_METTERE_PREP")[0],
                            ),
                            sem_roles,
                        )
                if hasattr(v, pred_syn_supp):
                    assign_and_increment(
                        t,
                        CausativeSemRole(
                            " ".join(x.occ for x in sogg),
                            ["fare"],
                            "ACTIVE",
                            data[getattr(v, pred_syn_supp).lemma]["verbo"],
                        ),
                        sem_roles,
                    )
                    if (
                        a_phrase_si := search_a_phrase(
                            v.get_next_block_tags(number_of_blocks=2)
                        )
                    ) and any(
                        x.startswith("PRED_SEM") or x.startswith(pred_syn_supp)
                        for x in dir(v)
                    ):
                        if v.can_assign_sem_roles():
                            assign_and_increment(
                                v,
                                SuppSemRole(
                                    " ".join(x.occ for x in a_phrase_si),
                                    [data[getattr(v, pred_syn_supp).lemma]["verbo"]],
                                    "ACTIVE",
                                ),
                                sem_roles,
                            )

        if (
            (
                a_phrase_si := search_a_phrase(
                    t.get_next_block_tags(number_of_blocks=2)
                )
                or (
                    is_dativo_clitic := [
                        x for x in t.get_same_block_tags() if x.note == "OGG INDIR"
                    ]
                )
            )
            and any(x.startswith("PRED_SEM") for x in dir(v))
            and v.can_assign_sem_roles()
        ):
            if not a_phrase_si:
                a_phrase_si = is_dativo_clitic
            if v.lemma in trivalent_verbs:
                assign_and_increment(
                    v,
                    DativeSemRole(" ".join(x.occ for x in a_phrase_si), [v.lemma]),
                    sem_roles,
                )
            else:
                assign_and_increment(
                    v,
                    OrdinarySemRole(
                        " ".join(x.occ for x in a_phrase_si), [v.lemma], "ACTIVE"
                    ),
                    sem_roles,
                )
        if da_phrase_si := search_da_phrase(t.get_next_block_tags(number_of_blocks=4)):
            if hasattr(v, "PRED_SEM_ORD"):
                assign_and_increment(
                    v,
                    OrdinarySemRole(
                        " ".join(x.occ for x in da_phrase_si), [v.lemma], "ACTIVE"
                    ),
                    sem_roles,
                )
            elif hasattr(v, "PRED_SYN_ATE") and v.can_assign_sem_roles():
                ate_noun = getattr(v, "PRED_SYN_ATE")
                if ate_noun in ate_multiwords:
                    d = ate_multiwords
                    verb = d[ate_noun]
                elif ate_noun in ate_multiwords_insultare:
                    verb = "insultare"
                elif ate_noun in ate_multiwords_colpire:
                    verb = "colpire"
                else:
                    raise ValueError
                assign_and_increment(
                    v,
                    AteSemRole(
                        " ".join(x.occ for x in da_phrase_si),
                        [verb, ate_noun],
                        "ACTIVE",
                        [getattr(v, "PRED_SYN_ATE")],
                    ),
                    sem_roles,
                )
    elif t.is_passive():
        if hasattr(v, pred_sem_fare_caus):
            assign_and_increment(
                t,
                CausativeSemRole(
                    " ".join(x.occ for x in sogg), ["fare"], "PASSIVE", v.occ
                ),
                sem_roles,
            )
        if (
            (
                da_phrase_si := search_da_phrase(
                    t.get_next_block_tags(number_of_blocks=2)
                )
            )
            and any(x.startswith("PRED_SEM") for x in dir(v))
            and v.can_assign_sem_roles()
        ):
            assign_and_increment(
                t,
                CausativeSemRole(
                    " ".join(x.occ for x in da_phrase_si), ["fare"], "ACTIVE", v.occ
                ),
                sem_roles,
            )
    elif t.is_middle_pr():
        if any(x.startswith("PRED_SEM") for x in dir(v)):
            assign_and_increment(
                t,
                CausativeSemRole(
                    " ".join(x.occ for x in sogg), ["fare"], "ACTIVE", v.occ
                ),
                sem_roles,
            )
            if v.lemma not in all_intransitives and v.lemma not in trivalent_verbs:
                assign_and_increment(
                    v,
                    OrdinarySemRole(
                        " ".join(x.occ for x in sogg), [v.lemma], "PASSIVE"
                    ),
                    sem_roles,
                )
            if v.lemma in trivalent_verbs:
                assign_and_increment(
                    v,
                    DativeSemRole(" ".join(x.occ for x in sogg), [v.lemma]),
                    sem_roles,
                )
            if (
                da_phrase_si := search_da_phrase(
                    t.get_next_block_tags(number_of_blocks=2)
                )
            ) and any(x.startswith("PRED_SEM") for x in dir(v)):
                assign_and_increment(
                    v,
                    OrdinarySemRole(
                        " ".join(x.occ for x in da_phrase_si), [v.lemma], "ACTIVE"
                    ),
                    sem_roles,
                )
        elif any(x.startswith("PRED_SYN_ATE") for x in dir(v)):
            verb = getattr(v, "PRED_SYN_ATE")
            f3 = None
            if verb in ate_multiwords:
                f3 = ate_multiwords[verb]
            elif verb in ate_multiwords_colpire:
                f3 = "colpire"
            elif verb in ate_multiwords_insultare:
                f3 = "insultare"
            if f3:
                assign_and_increment(
                    t,
                    CausativeSemRole(
                        " ".join(x.occ for x in sogg), ["fare"], "ACTIVE", f3
                    ),
                    sem_roles,
                )
            if (
                da_phrase_si := search_da_phrase(
                    t.get_next_block_tags(number_of_blocks=2)
                )
            ) and any(x.startswith("PRED_SEM") for x in dir(v)):
                assign_and_increment(
                    t,
                    OrdinarySemRole(
                        " ".join(x.occ for x in da_phrase_si), [v.lemma], "ACTIVE"
                    ),
                    sem_roles,
                )
