from typing import List

from ...Tag import Tag
from .search_det_np import find_bare_plural_noun, nomi_di_parentela, search_det_np
from .search_pro_pers__npr import search_pro_pers__npr
from .utils import delete_candidate
from .verb_support_nouns import verb_support_nouns


def candidates_handler(
    tags_blocchi_tra_sintagmi_verbali: List[List[Tag]], all_tags: List[Tag]
) -> List[List[List[int]]]:
    result = []
    done = set()

    for tags in tags_blocchi_tra_sintagmi_verbali:
        # Gli amici, le persone, ...
        find_det_np_result = search_det_np(tags, all_tags, done)

        # Giovanni, noi, te (esclude a Giovanni, a noi, etc.)
        find_pro_pers_npr_result = search_pro_pers__npr(tags)

        find_bare_noun_result = find_bare_plural_noun(all_tags, done)
        nomi_di_parentela_result = nomi_di_parentela(all_tags, done)
        verb_support_nouns_result = verb_support_nouns(all_tags, done)

        result.append(
            sorted(
                find_pro_pers_npr_result
                + find_det_np_result
                + find_bare_noun_result
                + nomi_di_parentela_result
                + verb_support_nouns_result,
                key=lambda x: x[0],
            )
        )

    candidates_flat = []
    for blocco_non_verb in result:
        for candidato in blocco_non_verb:
            candidates_flat.append(candidato)

    to_be_deleted = []

    # Starting from the shortest
    candidates_flat.sort(key=lambda x: len(x))

    # e.g., we remove [3] from [3, 4]
    for i, candidato in enumerate(candidates_flat):
        for _, altro_candidato in enumerate(candidates_flat[i + 1 :]):
            # if all items in [3] are contained in [3, 4]
            # flag [3] for deletion
            if all(x in altro_candidato for x in candidato):
                to_be_deleted.append(candidato)

    for tbd in to_be_deleted:
        delete_candidate(result, tbd)

    return result
