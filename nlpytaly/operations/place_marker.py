from typing import List

from ..Tag import Tag
from ..data.places import places


def place_marker(tags: List[Tag]) -> None:
    for t in tags:
        if t._lemma in places:
            t.note = "luogo"
