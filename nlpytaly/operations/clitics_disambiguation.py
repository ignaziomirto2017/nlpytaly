from typing import List

from ..Tag import Tag


def s_p_disambiguation(tags: List[Tag]) -> None:
    for t in tags:
        if t.occ in ["gli", "le"]:
            if t.is_in_SV_block():
                t.number = "s|p"
            else:
                t.number = "p"


def se_gli_la_le_disambiguation(tags: List[Tag], indici_verbi_flessi: List[List[int]]):
    for group in indici_verbi_flessi:
        block: List[Tag] = tags[group[0]].get_same_block_tags()
        for tag in block:
            if tag.occurrence in ["se", "gli", "la", "le"]:
                if tag.occurrence == "gli":
                    tag.note = "OGG INDIR"
                elif tag.occurrence == "la":
                    tag.note = "OGG DIR"
                elif tag.occurrence == "le":
                    tag.note = "OGG (IN)DIR"
                elif tag.occurrence == "se":
                    tag.lemma = "si"
                tag.pos = "CLIT"


def clitics_disambiguation(tags: List[Tag], indici_verbi_flessi: List[List[int]]):
    s_p_disambiguation(tags)
    se_gli_la_le_disambiguation(tags, indici_verbi_flessi)
