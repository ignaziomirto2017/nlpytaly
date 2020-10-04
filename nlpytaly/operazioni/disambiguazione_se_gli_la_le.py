from typing import List

from ..Tag import Tag


def disambiguazione_clitici(tags: List[Tag], indici_verbi_flessi: List[List[int]]):
    disambiguazione_se_gli_la_le(tags, indici_verbi_flessi)


def disambiguazione_se_gli_la_le(tags: List[Tag], indici_verbi_flessi: List[List[int]]):
    for group in indici_verbi_flessi:
        block: List[Tag] = tags[group[0]].get_same_block_tags()
        for tag in block:
            if tag.occorrenza in ["se", "gli", "la", "le"]:
                if tag.occorrenza == "gli":
                    tag.note = "OGG INDIR"
                elif tag.occorrenza == "la":
                    tag.note = "OGG DIR"
                elif tag.occorrenza == "le":
                    tag.note = "OGG (IN)DIR"
                elif tag.occorrenza == "se":
                    tag.lemma = "si"
                tag.pos = "CLIT"
