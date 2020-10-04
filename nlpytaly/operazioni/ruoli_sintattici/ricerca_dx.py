from typing import List

from ...Tag import Tag


def candidato_piu_vicino_dx_verbs(
    indici_SV: List[List[int]],
    indici_candidati: List[List[int]],
    tags: List[Tag],
    exclusions,
    step: int,
):
    result = []
    for x in indici_SV[::-1]:
        last_index = x[-1]
        for candidato in indici_candidati:
            if (
                last_index < candidato[0]
                and tags[candidato[0]].block <= tags[last_index].block + step
            ):
                if not any([x in exclusions for x in candidato]):
                    result.append([candidato, x])
                    indici_candidati.remove(candidato)
                    break
    return result
