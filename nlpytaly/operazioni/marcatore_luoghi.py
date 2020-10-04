from typing import List

from ..Tag import Tag
from ..data.luoghi import luoghi


def marca_luoghi(tags: List[Tag]) -> None:
    for t in tags:
        if t._lemma in luoghi:
            t.note = "luogo"
