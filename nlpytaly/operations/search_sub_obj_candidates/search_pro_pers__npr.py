from itertools import takewhile
from typing import List

from ...Tag import Tag

pronomi = [
    "egli",
    "esso",
    "essa",
    "essi",
    "esse",
    "io",
    "lei",
    "loro",
    "lui",
    "me",
    "noi",
    "te",
    "tu",
    "voi",
]


def search_pro_pers__npr(tags: List[Tag]) -> List[List[int]]:
    result = []

    done = set()
    for i, t in enumerate(tags):
        if t.occurrence in pronomi or t.pos == "NPR":
            if (
                i > 0
                and tags[i - 1].is_preposition()
                or tags[i - 1].is_article()
                or tags[i - 1].is_adjective()
            ):
                continue
            else:
                if t.occurrence in pronomi:
                    if not t.is_pro_pers():
                        continue
                    t._is_sub_obj_candidate = True
                    tmp = [t] + list(
                        takewhile(
                            lambda x: x.pos == "NOM",
                            (tags[j] for j in range(len(tags)) if j > i),
                        )
                    )
                    if any(j.index in done for j in tmp):
                        continue
                    else:
                        result.append(list(j.index for j in tmp))
                        for k in tmp:
                            k._is_sub_obj_candidate = True
                            done.add(k.index)
                else:
                    if i >= 2 and tags[i - 1].pos == "NOM" and tags[i - 2].pos != "PRE":
                        pass
                    else:
                        tmp = list(
                            takewhile(
                                lambda x: x.pos == "NPR",
                                (tags[j] for j in range(len(tags)) if j >= i),
                            )
                        )
                        if any(j.index in done for j in tmp):
                            continue
                        else:
                            result.append(list(j.index for j in tmp))
                            for k in tmp:
                                k._is_sub_obj_candidate = True
                                done.add(k.index)
    return result
