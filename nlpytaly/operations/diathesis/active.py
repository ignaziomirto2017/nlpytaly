from typing import List

from ...data.verbs.class_2_verbs import class_2_verbs
from ...Tag import Tag
from .utils import assign


def active_mRFL(tags: List[Tag]):
    blocks_done = set()
    for t in (_ for _ in tags if _.block not in blocks_done):
        sb_tags = t.get_same_block_tags()
        if t.is_in_SV_block():
            if t.is_middle_pr() or t.is_passive() or t.is_middle_mr():
                pass
            else:
                if any(
                    x.lemma in {"essere"} | class_2_verbs for x in sb_tags
                ) and not any(x.is_causative_fare for x in sb_tags):
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
