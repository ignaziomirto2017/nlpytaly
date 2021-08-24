from typing import List

from ...Tag import Tag


def nearest_candidate_right(
    indici_SV: List[List[int]],
    candidates_indexes: List[List[int]],
    tags: List[Tag],
    exclusions,
    step: int,
):
    result = []
    for x in indici_SV[::-1]:
        last_index = x[-1]
        for candidate in candidates_indexes:
            if (
                last_index < candidate[0]
                and tags[candidate[0]].block <= tags[last_index].block + step
            ):
                if not any([x in exclusions for x in candidate]):
                    result.append([candidate, x])
                    candidates_indexes.remove(candidate)
                    break
    return result
