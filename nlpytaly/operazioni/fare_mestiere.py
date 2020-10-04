from typing import List

from ..Tag import Tag
from ..Utils import increment_blocks
from ..data.articoli_det import articoli_det
from ..data.lista_mestieri import lista_mestieri

pred_name = "PRED_MEST"


def trova_rs_mestieri_mark(tags: List[Tag]) -> List[int]:
    esclusioni_od: List[int] = []
    for t in tags:
        if t.lemma in lista_mestieri and tags[t.index - 1].occorrenza in articoli_det:
            for p in t.get_prev_block_tags():
                if p.lemma == "fare":
                    t.note = pred_name
                    esclusioni_od.append(t.index)
                    increment_blocks(tags, t.index - 1, t.index)
                    break

    return esclusioni_od
