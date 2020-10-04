from typing import List

from ..Tag import Tag
from ..data.locuzioni_data import data


def locuzioni(tags: List[Tag]):
    verifica(data, tags, tags, [])
    for i, t in enumerate(tags):
        t.index = i


def verifica(d: dict, tags: list, original_tags: list, tmp=None):
    if tmp is None:
        tmp = []

    for i, t in enumerate(tags):
        if t.occ in d:
            tmp.append(t)
            if d[t.occ].get("end", False):

                index, pos = tmp[0].index, d[t.occ].get("pos", "ADV")
                original_tags[index].pos = pos
                original_tags[index].occorrenza = " ".join(t.occ for t in tmp)
                original_tags[index].lemma = "multiword"
                original_tags[index].note = d[t.occ]["sinonimo"]
                del original_tags[tmp[0].index + 1 : tmp[-1].index + 1]
                tmp = []
            else:
                verifica(d[t.occ], tags[i:], original_tags, tmp)
