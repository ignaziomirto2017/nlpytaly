from typing import List

from .find_det_NP import find_det_NP
from .find_pro_pers_npr import find_pro_pers_npr
from ...Tag import Tag


def handler(tags_blocchi_tra_sintagmi_verbali: List[List[Tag]], all_tags: List[Tag]):
    result = []
    for tags in tags_blocchi_tra_sintagmi_verbali:
        # Gli amici, le persone, ...
        find_det_np_result = find_det_NP(tags, all_tags)

        # Giovanni, noi, te (esclude a Giovanni, a noi, etc.)
        find_pro_pers_npr_result = find_pro_pers_npr(tags)
        result.append(
            sorted(find_pro_pers_npr_result + find_det_np_result, key=lambda x: x[0])
        )
    return result
