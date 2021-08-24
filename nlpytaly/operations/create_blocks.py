from typing import List

from ..Tag import Tag


def increment(tags: List[Tag], i: int):
    for j in range(i, len(tags)):
        tags[j].block += 1


def decrement(tags: List[Tag], i: int):
    for j in range(i, len(tags)):
        tags[j].block -= 1


def fix(tags: List[Tag]):
    for i in range(len(tags) - 1):
        if tags[i + 1].block - tags[i].block > 1:
            decrement(tags, i + 1)


def create_blocks(tags: List[Tag], indici_verbi_flessi: List[List[int]]):
    for blocco_indici in indici_verbi_flessi:
        leftmost = blocco_indici[0]
        if leftmost == 0:
            for b in blocco_indici:
                tags[b].block = 1
        else:
            tmp = tags[leftmost - 1].block + 1
            for b in blocco_indici:
                tags[b].block = tmp
            increment(tags, blocco_indici[-1] + 1)
    for t in tags:
        if t.occurrence in ["e", "ed"]:
            increment(tags, t.index + 0)  # incrementiamo dalla posizione stessa
        if t.occurrence in list(",.;:!?") + [
            "che",
            "ma",
            "io",
            "tu",
            "lei",
            "lui",
            "esso",
            "essa",
            "noi",
            "voi",
            "essi",
            "esse",
            "loro",
            "mentre",
        ]:
            increment(tags, t.index + 1)
    fix(tags)
