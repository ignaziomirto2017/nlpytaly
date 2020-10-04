from typing import List

from ..operazioni.formazioni.formazione_infinito import formazione_infinito
from ..Tag import Tag
from ..data.ambiguo_noun_verb import ambiguo_noun_verb, data, part_pass


def disambigua_nome_verb(tags: List[Tag]):
    for t in tags:
        if t.occorrenza in ambiguo_noun_verb:
            if t.lemma == "verso":
                continue
            # e.g. consegna la merce
            elif t.index == 0:
                t.pos = "VER:pres"
                t.lemma = formazione_infinito(t.occorrenza)
                continue
            else:
                prev = t.get_tags_by_indexes(1, 1)[0]
                if prev.pos in data or prev.is_inflected_verb():
                    t.pos = "NOM"
                else:
                    t.pos = "VER:pres"
                    t.lemma = formazione_infinito(t.occorrenza)
        elif t.occorrenza in part_pass:
            prev = t.get_tags_by_indexes(1, 1)[0]
            if prev.is_verb() or prev.is_adverb():
                t.pos = "VER:pper"
                t.lemma = formazione_infinito(t.occorrenza)
