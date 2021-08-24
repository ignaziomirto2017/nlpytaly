from typing import List

from ...Tag import Tag
from ...data.verbs.intransitives import all_intransitives

verbi_copulativi = {
    "divenire",
    "diventare",
    "parere",
    "sembrare",
}
verbi_intransitivi_non_copulativi = all_intransitives - verbi_copulativi


def nearest_candidate_left(
    indici_SV: List[List[int]],
    indici_proclisi: List[List[int]],
    candidates_indexes: List[List[int]],
    tags: List[Tag],
    step: int,
    d,
):
    result = []
    to_delete = []
    for j in range(len(indici_SV)):
        x = indici_SV[j]
        first_index = x[0]
        for i in reversed(candidates_indexes):
            if (
                first_index - i[0] >= 0
                and tags[first_index].block - step
                <= tags[i[0]].block
                <= tags[first_index].block
            ):
                verbo = tags[first_index + len(indici_proclisi[j])]
                candidate = tags[i[0]]
                # Mia zia viaggia => saltiamo "mia" perché è di prima persona
                if candidate.is_pro_poss():
                    candidate = candidate.next()
                if verbo.match_pn(candidate):
                    v_block = tags[first_index].get_same_block_tags()
                    if (
                        any(tmp.has_subject for tmp in v_block)
                        or v_block[0].is_impersonal()
                    ):
                        break
                    result.append([i, x])
                    v_block = [x for x in v_block if not x.is_aux() and x.is_verb()]
                    if v_block:
                        verb = v_block[0].lemma
                        if (
                            verb in verbi_intransitivi_non_copulativi
                            or v_block[0].is_passive()
                        ) and not any(x.is_causative_fare for x in v_block):
                            to_delete.append(x)
                        d[tuple(x)] = True
                        for tmp in v_block:
                            tmp.has_subject = True
                        candidates_indexes.remove(i)
                        break
    for td in to_delete:
        indici_SV.remove(td)
    return result
