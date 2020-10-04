from typing import List

from .utils import assign
from ...Tag import Tag
from ...data.verbi.verbi_classe_2 import verbi_classe_2


def diatesi_attiva_mRFL(tags: List[Tag]):
    blocks_done = set()
    for t in (_ for _ in tags if _.block not in blocks_done):
        sb_tags = t.get_same_block_tags()
        if t.is_in_SV_block():
            if t.is_middle_pr() or t.is_passive():
                pass
            else:
                if any(
                    x.lemma in {"essere"} | verbi_classe_2 for x in sb_tags
                ) and not any(x.is_fare_causativo for x in sb_tags):
                    assign(tags, t, "MIDDLE_MR")
                elif (
                    any(x.lemma in ["volere"] for x in sb_tags)
                    and any(x.lemma in ["ci", "c'"] for x in sb_tags)
                    and t.get_same_block_tags()[-1].lemma != "bene"
                ):
                    assign(tags, t, "MIDDLE_MR")
                else:
                    assign(tags, t, "ACTIVE")
        blocks_done.add(t.block)
