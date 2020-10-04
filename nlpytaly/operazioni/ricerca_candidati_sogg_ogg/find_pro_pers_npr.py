from itertools import takewhile
from typing import List

from ...Tag import Tag

pronomi = [
    "egli",
    "essi",
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


def find_pro_pers_npr(tags: List[Tag]):
    result = []

    done = set()
    for i, t in enumerate(tags):
        if t.occorrenza in pronomi or t.pos == "NPR":
            if i > 0 and tags[i - 1].is_preposition() or tags[i - 1].is_article():
                continue
            else:
                if t.occorrenza in pronomi:
                    if not t.is_pro_pers():
                        continue
                    t.is_candidate = True
                    tmp = [t] + list(
                        takewhile(
                            lambda x: x.pos == "NOM",
                            (tags[j] for j in range(len(tags)) if j > i),
                        )
                    )
                    if any(j.index in done for j in tmp):
                        continue
                    else:
                        result.append(tuple(j.index for j in tmp))
                        for k in tmp:
                            k.is_candidate = True
                            done.add(k.index)
                else:
                    if (
                        i >= 2
                        and tags[i - 1].pos == "NOM"
                        and tags[i - 2].pos != "PREP"
                    ):
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
                            result.append(tuple(j.index for j in tmp))
                            for k in tmp:
                                k.is_candidate = True
                                done.add(k.index)
    return result
