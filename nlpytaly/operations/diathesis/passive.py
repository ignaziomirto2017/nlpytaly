from typing import List

from ...Tag import Tag
from .utils import assign


def passive(tags: List[Tag], notes: List[str]):
    blocks_done = set()
    for t in tags:
        if t.is_in_SV_block() and t.block not in blocks_done:
            if any(
                x in {"lo", "la", "li", "si"} for x in t.get_same_block_occurrences()
            ):
                continue
            sb_tags = list(filter(lambda x: x.is_verb(), t.get_same_block_tags()))
            match_data = [[x.lemma, x.pos] for x in sb_tags]
            match match_data:
                case [[verb, _], [_, "VER:pper"]]:
                    if verb in {"essere", "rimanere", "venire"}:
                        assign(tags, t, "PASSIVE")
                        blocks_done.add(t.block)
                case [["essere", _], [verb, "VER:pper"], [_, "VER:pper"], *_]:
                    if verb in {"andare", "rimanere", "stare"}:
                        assign(tags, t, "PASSIVE", force=True)
                        blocks_done.add(t.block)
                case [[verb, _], [_, "VER:pper"], [_, "VER:infi"]]:
                    if verb in {"essere", "venire"}:
                        assign(tags, t, "PASSIVE")
                        blocks_done.add(t.block)
