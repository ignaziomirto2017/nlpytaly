from typing import List, Tuple

import more_itertools as mit

from ..Tag import Tag


def get_blocchi_intermedi(
    tags: List[Tag], indici_verbi_flessi: List[List[int]]
) -> Tuple[List[List[int]], List[List[Tag]], List[str]]:
    blocchi_tra_sintagmi_verbali: List[List[int]] = []
    for i in range(len(indici_verbi_flessi)):
        if i == 0:
            if indici_verbi_flessi[0][0] == 0:
                blocchi_tra_sintagmi_verbali.append([])
            else:
                blocchi_tra_sintagmi_verbali.append(
                    [0, max(indici_verbi_flessi[0][0] - 1, 0)]
                )
        else:
            first = min(indici_verbi_flessi[i - 1][-1] + 1, len(tags) - 1)
            last = min(indici_verbi_flessi[i][0] - 1, len(tags) - 1)
            blocchi_tra_sintagmi_verbali.append([first, last])
    if indici_verbi_flessi[-1][-1] == len(tags) - 1:
        blocchi_tra_sintagmi_verbali.append([])
    else:
        blocchi_tra_sintagmi_verbali.append(
            [min(indici_verbi_flessi[-1][-1] + 1, len(tags) - 1), len(tags) - 1]
        )

    all_indexes = list(range(len(tags)))
    indexes_not_to_print = []
    for group in indici_verbi_flessi:
        for index in group:
            indexes_not_to_print.append(index)
    indexes_to_print = [x for x in all_indexes if x not in indexes_not_to_print]
    grouped_itp = [list(group) for group in mit.consecutive_groups(indexes_to_print)]
    # itp: indexes to print
    tags_blocchi_tra_sintagmi_verbali = []
    for group in grouped_itp:
        tags_blocchi_tra_sintagmi_verbali.append([tags[index] for index in group])
    parole_blocchi_tra_sintagmi_verbali: List[str] = []
    for tags in tags_blocchi_tra_sintagmi_verbali:
        parole_blocchi_tra_sintagmi_verbali.append(
            " ".join([x.occorrenza for x in tags])
        )
    return (
        blocchi_tra_sintagmi_verbali,
        tags_blocchi_tra_sintagmi_verbali,
        parole_blocchi_tra_sintagmi_verbali,
    )
