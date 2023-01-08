from typing import List

from nlpytaly.operations.semantic_roles.utils import assign_and_increment

from ...data.mettere_prep import mettere_prep_dict
from ...Tag import Tag
from ...Utils import mark_tag, search_da_phrase
from .pred_assigners import (
    pred_sem_fare_caus,
    pred_sem_mettere_prep,
    pred_syn_mettere_prep,
    pred_syn_mettere_prep_ov,
)
from .SemRole.SemRole import MetterePrepSemRole


def mark_mettere_prep(tags: List[Tag]):
    for t in tags:
        if t.lemma in mettere_prep_dict:
            p_tags = t.get_prev_block_tags(step=2, number_of_blocks=2)
            s_tags = [tmp for tmp in t.get_same_block_tags() if tmp.index > t.index]

            for t_noun in s_tags:
                if t_noun.occ in mettere_prep_dict[t.lemma]:
                    break
            else:
                continue

            for v in p_tags:
                if v.lemma in {"mettere", "essere"}:
                    mark_tag(
                        v,
                        pred_syn_mettere_prep,
                        (mettere_prep_dict[t.lemma][t_noun.occ]["v"], (t, t_noun)),
                    )
                    mark_tag(t_noun, pred_sem_mettere_prep, v)
                    v.set_max_assignable_sem_roles(2)
            else:
                if not any(
                    x.is_noun()
                    for x in (y for y in t.get_prev_block_tags() if y.index < t.index)
                ):
                    break
                assignee = [
                    x
                    for x in tags
                    if x.index < t.index
                    and x.block == t.block - 1
                    and (x.is_article() or x.is_noun())
                ]
                mark_tag(
                    t,
                    pred_syn_mettere_prep_ov,
                    {
                        "assignee": assignee,
                        "verb": mettere_prep_dict[t.lemma][t_noun.occ]["v"],
                        "t_noun": t_noun,
                    },
                )
                t.set_max_assignable_sem_roles(1)


def assign_mettere_prep(od, sem_roles, sogg: List[Tag], t: Tag, v, amb: List[Tag]):
    is_fare_caus = any(hasattr(x, pred_sem_fare_caus) for x in t.get_same_block_tags())
    v, noun = v[0], v[1]
    sogg = [Tag(t.cov_sub, "-", "-")] if (not sogg) else sogg
    if t.is_active():
        if is_fare_caus:
            if da_phrase_si := search_da_phrase(
                t.get_next_block_tags(number_of_blocks=4)
            ):
                assign_and_increment(
                    t,
                    MetterePrepSemRole(
                        " ".join(x.occ for x in da_phrase_si), [v], "ACTIVE", noun
                    ),
                    sem_roles,
                )
            else:
                t.assignable_sem_roles -= 1

        if od:
            assign_and_increment(
                t,
                MetterePrepSemRole(" ".join(x.occ for x in od), [v], "PASSIVE", noun),
                sem_roles,
            )

        # Se non ambiguo, assegna rs a sogg
        if amb is None:
            assign_and_increment(
                t,
                MetterePrepSemRole(" ".join(x.occ for x in sogg), [v], "ACTIVE", noun),
                sem_roles,
            )
        # Se ambiguo, nel caso di MetterePrep, si tratta sicuramente di OD
        # e.g., Ha messo il sospettato sotto sorveglianza
        else:
            assign_and_increment(
                t,
                MetterePrepSemRole(" ".join(x.occ for x in amb), [v], "PASSIVE", noun),
                sem_roles,
            )
            assign_and_increment(
                t, MetterePrepSemRole("LUI|LEI", [v], "ACTIVE", noun), sem_roles
            )

    elif t.is_passive():
        assign_and_increment(
            t,
            MetterePrepSemRole(" ".join(x.occ for x in sogg), [v], "PASSIVE", noun),
            sem_roles,
        )
        if da_phrase_si := search_da_phrase(t.get_next_block_tags(number_of_blocks=2)):
            assign_and_increment(
                t,
                MetterePrepSemRole(
                    " ".join(x.occ for x in da_phrase_si), [v], "ACTIVE", noun
                ),
                sem_roles,
            )
    elif t.is_middle_mr() and t.lemma == "essere" and amb is None:
        assign_and_increment(
            t,
            MetterePrepSemRole(" ".join(x.occ for x in sogg), [v], "PASSIVE", noun),
            sem_roles,
        )
    elif t.is_middle_pr():
        assign_and_increment(
            t,
            MetterePrepSemRole(" ".join(x.occ for x in sogg), [v], "ACTIVE_SI", noun),
            sem_roles,
        )


def assign_mettere_prep_ov(sem_roles, t, data):
    # ov = omitted verb
    # L'amico _sotto accusa_ è scappato
    # t => sotto
    # v => assignee
    verb = data["verb"]
    assignee = data["assignee"]
    t_noun = data["t_noun"]
    is_mettere_prep = any(
        hasattr(x, pred_sem_mettere_prep) for x in t.get_same_block_tags()
    )
    if not is_mettere_prep:
        assign_and_increment(
            t,
            MetterePrepSemRole(
                " ".join(x.occ for x in assignee),
                [verb],
                "PASSIVE",
                non_verbal_origin=[t_noun],
            ),
            sem_roles,
        )
