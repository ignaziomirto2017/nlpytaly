from typing import List

from ..data.ambiguous_noun_verb import ambiguous_noun_verb, data, past_part
from ..operations.formations.infinitive_formation import infinitive_formation
from ..operations.formations.past_part_formation import past_part_formation
from ..Tag import Tag


def _get_person(occ: str):
    last_char = occ[-1]
    if last_char == "o":
        person = 1
    elif last_char == "i":
        person = 2
    else:
        person = 3
    return person


def _get_gender_number(occ: str):
    last_char = occ[-1]
    if last_char == "o":
        gender, number = "m", "s"
    elif last_char == "i":
        gender, number = "m", "p"
    elif last_char == "a":
        gender, number = "f", "s"
    elif last_char == "e":
        gender, number = "f", "p"

    return gender, number


def noun_verb_disambiguation(tags: List[Tag]):
    for t in tags:
        prev: Tag = t.prev()
        person = _get_person(t.occ)
        if t.occ in ambiguous_noun_verb:
            if t.lemma == "verso":
                continue
            # e.g. consegna la merce, Tronco, Sparo
            elif t.index == 0:
                t.pos = "VER:pres"
                t.lemma = infinitive_formation(t.occ)
                t.set_pn(person, "s")
                continue
            else:
                if prev.pos in data or prev.is_inflected_verb():
                    if not t.is_noun():
                        t.pos = "NOM"
                        t.lemma = "-"
                else:
                    t.pos = "VER:pres"
                    t.lemma = infinitive_formation(t.occ)
                    t.set_pn(person, "s")
        elif t.occ in past_part and prev:
            if prev.is_verb() or prev.is_adverb():
                t.pos = "VER:pper"
                t.lemma = infinitive_formation(t.occ)
                g, n = _get_gender_number(t.occ)
                t.set_gn(g, n)
            elif prev.is_article():
                t.pos = "NOM"
                t.lemma = past_part_formation(t.lemma, female=True)
