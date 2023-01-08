from typing import List, Set

from ...data.ate_multiwords import (
    ate_multiwords,
    ate_multiwords_colpire,
    ate_multiwords_insultare,
    cognate_ate_multiwords,
    synonyms,
)
from ...Tag import Tag
from ...Utils import increment_blocks, mark_tag, search_da_phrase
from .pred_assigners import pred_sem_ate, pred_sem_fare_caus, pred_syn_ate
from .SemRole.SemRole import AteSemRole
from .utils import assign_and_increment

multiwords: Set[str] = (
    set(ate_multiwords.keys()) | ate_multiwords_colpire | ate_multiwords_insultare
)


def mark_ate_suffix(tags: List[Tag]):
    for t in tags:
        if t.lemma == "prendere":
            pb_tags = t.get_prev_block_tags()
            nb_tags = t.get_next_block_tags(number_of_blocks=2)
            for tmp in pb_tags + nb_tags:
                if (
                    tmp.occ in multiwords
                    and tmp.index > 0
                    and tags[tmp.index - 1].lemma == "a"
                ):
                    # Per gestire i casi come prendere a calci = prendere a pedate
                    occ = tags[tmp.index].occ
                    if occ in synonyms:
                        occ = synonyms[occ]
                    mark_tag(t, pred_syn_ate, occ)
                    mark_tag(tags[tmp.index], pred_sem_ate, t)
                    increment_blocks(tags, tmp.index - 1, tmp.index)
                    t.set_max_assignable_sem_roles(2)


def assign_ate_suffix(
    od, sem_roles, sogg: List[Tag], t: Tag, v, amb: List[Tag]  # e.g., pugnalate
):
    is_fare_caus = any(hasattr(x, pred_sem_fare_caus) for x in t.get_same_block_tags())
    if v in ate_multiwords:
        d = ate_multiwords
        verb = d[v]
    elif v in ate_multiwords_insultare:
        verb = "insultare"
    elif v in ate_multiwords_colpire:
        verb = "colpire"
    else:
        raise ValueError
    f2 = [verb, v]

    neg = t.is_negative_inflected_verb()

    # Remove last item if full cognate (pugnalare, pugnalate)
    if len(f2) == 2 and v in cognate_ate_multiwords:
        f2.pop()
    sogg = [Tag(t.cov_sub, "-", "-")] if (not sogg) else sogg
    if t.is_active():
        if not is_fare_caus:
            if not amb:
                assign_and_increment(
                    t,
                    AteSemRole(" ".join(x.occ for x in sogg), f2, "ACTIVE", [v], neg),
                    sem_roles,
                )
            else:
                assign_and_increment(
                    t,
                    AteSemRole(" ".join(x.occ for x in amb), f2, "PASSIVE", [v], neg),
                    sem_roles,
                )
                assign_and_increment(
                    t, AteSemRole("LUI|LEI", f2, "ACTIVE", [v], neg), sem_roles
                )
        if od:
            assign_and_increment(
                t,
                AteSemRole(" ".join(x.occ for x in od), f2, "PASSIVE", [v], neg),
                sem_roles,
            )
    elif t.is_passive():
        assign_and_increment(
            t,
            AteSemRole(" ".join(x.occ for x in sogg), f2, "PASSIVE", [v], neg),
            sem_roles,
        )
        pb_tags = t.get_prev_block_tags()
        nb_tags = t.get_next_block_tags(number_of_blocks=3)
        if da_phrase_si := search_da_phrase(pb_tags + nb_tags):
            assign_and_increment(
                t,
                AteSemRole(
                    " ".join(x.occ for x in da_phrase_si), f2, "ACTIVE", [v], neg
                ),
                sem_roles,
            )
    elif t.is_middle_pr():
        # Max si è preso a schiaffi
        assign_and_increment(
            t,
            AteSemRole(" ".join(x.occ for x in sogg), f2, "PASSIVE", [v], neg),
            sem_roles,
        )
        if not is_fare_caus:
            assign_and_increment(
                t,
                AteSemRole(" ".join(x.occ for x in sogg), f2, "ACTIVE", [v], neg),
                sem_roles,
            )
        else:
            # Max si è fatto prendere a schiaffi da Luigi
            pb_tags = t.get_prev_block_tags()
            nb_tags = t.get_next_block_tags(number_of_blocks=3)
            if da_phrase_si := search_da_phrase(pb_tags + nb_tags):
                assign_and_increment(
                    t,
                    AteSemRole(
                        " ".join(x.occ for x in da_phrase_si), f2, "ACTIVE", [v], neg
                    ),
                    sem_roles,
                )
    elif t.is_past_participle():
        v_block = [x for x in t.get_same_block_tags() if x.index < t.index]
        assign_and_increment(
            t,
            AteSemRole(" ".join(x.occ for x in v_block), f2, "PASSIVE", [v], neg),
            sem_roles,
        )
