from typing import List

from ..data.places import places
from ..Tag import Tag


def place_marker(tags: List[Tag]) -> None:
    for t in tags:
        if t._lemma in places:
            t.note = "Place"
            t.place = True
