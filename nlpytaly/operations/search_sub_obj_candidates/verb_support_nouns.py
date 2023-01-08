from typing import List

from ...Tag import Tag
from ..semantic_roles.pred_assigners import pred_sem_supp


def verb_support_nouns(tags: List[Tag], candidates_indexes):
    result = []
    for t in tags:
        if hasattr(t, pred_sem_supp) and t.index not in candidates_indexes:
            sb = t.get_same_block_tags()
            # si evita di prendere nuovamente sostantivi come "multa" in "una multa"
            # mentre si prende "odio" in "prova odio"
            if sb:
                sb0: Tag = sb[0]
                if (
                    not sb0.is_article()
                    and not sb0.is_adjective()
                    and not sb0.is_preposition()
                    and not sb0.is_pro_pers()
                    and not sb0.is_pro_indef()
                    and not sb0.is_card()
                ):
                    result.append([t.index])
                    t._is_sub_obj_candidate = True
                    candidates_indexes.add(t.index)
    return result
