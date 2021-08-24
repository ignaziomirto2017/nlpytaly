from typing import List

from .search_det_np import search_det_np, find_bare_plural_noun, nomi_di_parentela
from .search_pro_pers__npr import search_pro_pers__npr
from ...Tag import Tag


def candidates_handler(
    tags_blocchi_tra_sintagmi_verbali: List[List[Tag]], all_tags: List[Tag]
) -> List[List[List[int]]]:
    result = []
    done = set()

    for tags in tags_blocchi_tra_sintagmi_verbali:
        # Gli amici, le persone, ...
        find_det_np_result = search_det_np(tags, all_tags)

        # Giovanni, noi, te (esclude a Giovanni, a noi, etc.)
        find_pro_pers_npr_result = search_pro_pers__npr(tags)

        find_bare_noun_result = find_bare_plural_noun(all_tags, done)
        nomi_di_parentela_result = nomi_di_parentela(all_tags, done)

        result.append(
            sorted(
                find_pro_pers_npr_result
                + find_det_np_result
                + find_bare_noun_result
                + nomi_di_parentela_result,
                key=lambda x: x[0],
            )
        )
    return result
