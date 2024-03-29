from typing import List

from ...Tag import Tag
from .maybe_partitive_nb import process_next_block
from .maybe_partitive_pb import process_prev_block
from .maybe_partitive_sb import process_same_block


def maybe_partitive(tags: List[Tag], notes: List[str]):
    blocks_done = set()
    pivot = ["del", "dello", "della", "dei", "degli", "delle", "dell'"]
    for t in tags:
        if t.occurrence in pivot:
            process_same_block(t.get_same_block_tags(), tags, notes, blocks_done, t)
            # ANASTROFE
            process_next_block(t.get_next_block_tags(), tags, notes, blocks_done, t)
            process_prev_block(t.get_prev_block_tags(), tags, notes, blocks_done, t)
