from typing import List

from ..Tag import Tag
from ..data.ambiguous_noun_verb import ambiguous_noun_verb, data, past_part
from ..operations.formations.infinitive_formation import infinitive_formation


def noun_verb_disambiguation(tags: List[Tag]):
    for t in tags:
        if t.occurrence in ambiguous_noun_verb:
            if t.lemma == "verso":
                continue
            # e.g. consegna la merce
            elif t.index == 0:
                t.pos = "VER:pres"
                t.lemma = infinitive_formation(t.occurrence)
                continue
            else:
                prev: Tag = t.get_tags_by_indexes(1, 1)[0]
                if prev.pos in data or prev.is_inflected_verb():
                    if not t.is_noun():
                        t.pos = "NOM"
                        t.lemma = "-"
                else:
                    t.pos = "VER:pres"
                    t.lemma = infinitive_formation(t.occurrence)
        elif t.occurrence in past_part:
            prev = t.get_tags_by_indexes(1, 1)[0]
            if prev.is_verb() or prev.is_adverb():
                t.pos = "VER:pper"
                t.lemma = infinitive_formation(t.occurrence)
