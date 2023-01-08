from collections import namedtuple
from typing import List

from ....Tag import Tag

GenderNumber = namedtuple("GenderNumber", ["gender", "number"])


_data = {
    "molto": GenderNumber("m", "s"),
    "molta": GenderNumber("f", "s"),
    "molti": GenderNumber("m", "p"),
    "molte": GenderNumber("f", "p"),
    "tanto": GenderNumber("m", "s"),
    "tanta": GenderNumber("f", "s"),
    "tanti": GenderNumber("m", "p"),
    "tante": GenderNumber("f", "p"),
    "numeroso": GenderNumber("m", "s"),
    "numerosa": GenderNumber("f", "s"),
    "numerosi": GenderNumber("m", "p"),
    "numerose": GenderNumber("f", "p"),
    "parecchio": GenderNumber("m", "s"),
    "parecchia": GenderNumber("f", "s"),
    "parecchi": GenderNumber("m", "p"),
    "parecchie": GenderNumber("f", "p"),
}

_lemmas = {"molto", "tanto", "numeroso", "parecchio"}


def quantifiers(tags: List[Tag]):
    for i, t in enumerate(tags):
        if t.lemma in _lemmas and i < len(tags) - 1:
            if t.next().is_noun():
                t.gender = _data[t.occ].gender
                t.number = _data[t.occ].number
