from typing import List

from .SemRole.SemRole import (
    OrdinarySemRole,
    CausativeSemRole,
    AteSemRole,
    DativeSemRole,
)
from .pred_assigners import *
from ...Tag import Tag
from ...Utils import (
    mark_tag,
    search_da_phrase,
    search_a_phrase,
)
from ...data.ate_multiwords import (
    ate_multiwords,
    ate_multiwords_colpire,
    ate_multiwords_insultare,
)
from ...data.verb_support import data
from ...data.verbs.intransitives import all_intransitives
from ...data.verbs.trivalent import trivalent_verbs


def mark_causative_fare(tags: List[Tag]):
    for t in tags:
        if t.lemma == "fare":
            if is_causative_fare := [
                x
                for x in t.get_same_block_tags()
                if "infi" in x.pos and t.index < x.index
            ]:
                t.is_causative_fare = True
                mark_tag(t, pred_sem_fare_caus, is_causative_fare[0])


def assign_causative_fare(sem_roles, sogg, t: Tag, v: Tag, sr_cov_subjects: dict):
    if t.is_active():
        if not sogg and t.cov_sub:
            sogg = [Tag(t.cov_sub, "-", "-")]
            sr_cov_subjects[(t.cov_sub, v.occ)] = True
        if sogg:
            for x in sogg:
                x.sem_role_inc(t.get_same_block_indexes())
                x.sem_role_set_max(1, t.get_same_block_indexes())
            if hasattr(t, pred_sem_fare_caus):
                if any(x.startswith("PRED_SEM") for x in dir(v)):
                    sem_roles.append(
                        CausativeSemRole(
                            " ".join(x.occ for x in sogg), ["fare"], "ACTIVE", v.occ
                        )
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
                            sem_roles.append(
                                CausativeSemRole(
                                    " ".join(x.occ for x in sogg),
                                    ["fare"],
                                    "ACTIVE",
                                    f3,
                                )
                            )
                    if hasattr(v, "PRED_SYN_METTERE_PREP"):
                        sem_roles.append(
                            CausativeSemRole(
                                " ".join(x.occ for x in sogg),
                                ["fare"],
                                "ACTIVE",
                                getattr(v, "PRED_SYN_METTERE_PREP")[0],
                            )
                        )
                    if hasattr(v, pred_syn_supp):
                        sem_roles.append(
                            CausativeSemRole(
                                " ".join(x.occ for x in sogg),
                                ["fare"],
                                "ACTIVE",
                                getattr(v, pred_syn_supp).lemma,
                            )
                        )
                        if (
                            a_phrase_si := search_a_phrase(
                                v.get_next_block_tags(number_of_blocks=2)
                            )
                        ) and any(
                            x.startswith("PRED_SEM") or x.startswith(pred_syn_supp)
                            for x in dir(v)
                        ):
                            sem_roles.append(
                                OrdinarySemRole(
                                    " ".join(x.occ for x in a_phrase_si),
                                    [data[getattr(v, pred_syn_supp).lemma]["verbo"]],
                                    "ACTIVE",
                                )
                            )
            if (
                a_phrase_si := search_a_phrase(
                    t.get_next_block_tags(number_of_blocks=2)
                )
            ) and any(x.startswith("PRED_SEM") for x in dir(v)):
                if v.lemma in trivalent_verbs:
                    sem_roles.append(
                        DativeSemRole(" ".join(x.occ for x in a_phrase_si), [v.lemma]),
                    )
                else:
                    sem_roles.append(
                        OrdinarySemRole(
                            " ".join(x.occ for x in a_phrase_si), [v.lemma], "ACTIVE"
                        )
                    )
            if da_phrase_si := search_da_phrase(
                t.get_next_block_tags(number_of_blocks=4)
            ):
                if hasattr(v, "PRED_SEM_ORD"):
                    sem_roles.append(
                        OrdinarySemRole(
                            " ".join(x.occ for x in da_phrase_si), [v.lemma], "ACTIVE",
                        )
                    )
                elif hasattr(v, "PRED_SYN_ATE"):
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
                    sem_roles.append(
                        AteSemRole(
                            " ".join(x.occ for x in da_phrase_si),
                            [verb, ate_noun],
                            "ACTIVE",
                            [getattr(v, "PRED_SYN_ATE")],
                        )
                    )
    elif t.is_passive():
        if hasattr(v, pred_sem_fare_caus):
            sem_roles.append(
                CausativeSemRole(
                    " ".join(x.occ for x in sogg), ["fare"], "PASSIVE", v.occ
                )
            )
        if (
            da_phrase_si := search_da_phrase(t.get_next_block_tags(number_of_blocks=2))
        ) and any(x.startswith("PRED_SEM") for x in dir(v)):
            sem_roles.append(
                CausativeSemRole(
                    " ".join(x.occ for x in da_phrase_si), ["fare"], "ACTIVE", v.occ
                )
            )
    elif t.is_middle_pr():
        if sogg:  # Risolve con "Si fa aiutare da alcuni amici"
            for x in sogg:
                x.sem_role_inc(t.get_same_block_indexes())
                x.sem_role_set_max(2, t.get_same_block_indexes())
            if hasattr(t, pred_sem_fare_caus):
                if any(x.startswith("PRED_SEM") for x in dir(v)):
                    sem_roles.append(
                        CausativeSemRole(
                            " ".join(x.occ for x in sogg), ["fare"], "ACTIVE", v.occ
                        )
                    )
                    if (
                        v.lemma not in all_intransitives
                        and v.lemma not in trivalent_verbs
                    ):
                        sem_roles.append(
                            OrdinarySemRole(
                                " ".join(x.occ for x in sogg), [v.lemma], "PASSIVE"
                            ),
                        )
                    if v.lemma in trivalent_verbs:
                        sem_roles.append(
                            DativeSemRole(" ".join(x.occ for x in sogg), [v.lemma]),
                        )
                    if (
                        da_phrase_si := search_da_phrase(
                            t.get_next_block_tags(number_of_blocks=2)
                        )
                    ) and any(x.startswith("PRED_SEM") for x in dir(v)):
                        sem_roles.append(
                            OrdinarySemRole(
                                " ".join(x.occ for x in da_phrase_si),
                                [v.lemma],
                                "ACTIVE",
                            )
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
                        sem_roles.append(
                            CausativeSemRole(
                                " ".join(x.occ for x in sogg), ["fare"], "ACTIVE", f3
                            )
                        )
                    if (
                        da_phrase_si := search_da_phrase(
                            t.get_next_block_tags(number_of_blocks=2)
                        )
                    ) and any(x.startswith("PRED_SEM") for x in dir(v)):
                        sem_roles.append(
                            OrdinarySemRole(
                                " ".join(x.occ for x in da_phrase_si),
                                [v.lemma],
                                "ACTIVE",
                            )
                        )
