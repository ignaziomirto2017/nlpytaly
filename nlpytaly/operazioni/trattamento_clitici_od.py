from typing import List

from ..Tag import Tag
from ..Utils import get_SOGG_OD_for_tag_occurrences
from ..data.clitici import clitici
from ..data.verbi.intransitives import all_intransitives


def tratta_clitici(tags: List[Tag], ruoli_sintattici_result) -> None:
    for t in tags:
        if t.is_in_SV_block():
            v_block = t.get_same_block_tags()
            if not any(x.lemma in all_intransitives for x in v_block):
                _, o, _, _ = get_SOGG_OD_for_tag_occurrences(
                    t, tags, ruoli_sintattici_result
                )
                if not o and v_block[0].is_active():
                    for tag in v_block:
                        if tag.lemma in clitici:
                            ruoli_sintattici_result[(tag.index,)] = (
                                "OD",
                                t.get_same_block_indexes(),
                            )
