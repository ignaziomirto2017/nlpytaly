from typing import List

from ...data.multiwords import _lemma, _pos, _syn, data
from ...Tag import Tag


def restore_indexes(tags):
    for i, t in enumerate(tags):
        t.index = i


def check(d: dict, tags: list, original_tags: List[Tag], tmp=None):
    if tmp is None:
        tmp = []

    for i, t in enumerate(tags):
        if t.occ in d:
            tmp.append(t)
            if d[t.occ].get("end", False):
                # retrieve index and PoS
                index, pos = tmp[0].index, d[t.occ].get(_pos, "ADV")
                original_tags[index].pos = pos
                original_tags[index].occurrence = " ".join(t.occ for t in tmp)

                original_tags[index].lemma = _lemma
                original_tags[index].note = d[t.occ][_syn]
                del original_tags[tmp[0].index + 1 : tmp[-1].index + 1]
                tmp = []
            else:
                check(d[t.occ], tags[i:], original_tags, tmp)


def multiwords(tags: List[Tag]):
    check(data, tags, tags, [])
    restore_indexes(tags)
