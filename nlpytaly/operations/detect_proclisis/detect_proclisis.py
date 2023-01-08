from typing import List, Tuple

from ...data.clitics import clitics, clitics_atm_1
from ...Tag import Tag


def detect_proclisis(tags: List[Tag]) -> Tuple[List[List[str]], List[List[int]]]:
    proclisis_list: List[List[Tag]] = []
    for i, t in enumerate(tags):
        clitic: List[Tag] = []
        if t.is_inflected_verb():
            if (
                i >= 4
                and tags[i - 4].lemma == "non"
                and tags[i - 3].occurrence in clitics
                and tags[i - 2].occurrence in clitics
                and tags[i - 1].occurrence in clitics_atm_1
            ):
                clitic.append(tags[i - 4])
                clitic.append(tags[i - 3])
                clitic.append(tags[i - 2])
                clitic.append(tags[i - 1])
            elif (
                i >= 3
                and tags[i - 3].occurrence in clitics
                and tags[i - 2].occurrence in clitics
                and tags[i - 1].occurrence in clitics_atm_1
            ):
                clitic.append(tags[i - 3])
                clitic.append(tags[i - 2])
                clitic.append(tags[i - 1])
            elif (
                i >= 3
                and tags[i - 3].lemma == "non"
                and tags[i - 2].occurrence
                and tags[i - 1].occurrence in clitics_atm_1
            ):
                clitic.append(tags[i - 3])
                clitic.append(tags[i - 2])
                clitic.append(tags[i - 1])
            elif (
                i >= 2
                and tags[i - 2].lemma == "non"
                and tags[i - 1].occurrence in clitics
            ):
                clitic.append(tags[i - 2])
                clitic.append(tags[i - 1])
            elif (
                i >= 2
                and tags[i - 2].occurrence in clitics
                and tags[i - 1].occurrence in clitics
            ):
                clitic.append(tags[i - 2])
                clitic.append(tags[i - 1])

            elif i >= 1 and tags[i - 1].occurrence in clitics_atm_1:
                clitic.append(tags[i - 1])

            for item in clitic:
                item.is_proclisis = True
            proclisis_list.append(clitic[:])
    indexes = []
    strings = []
    for item in proclisis_list:
        indexes.append([x.index for x in item])
        strings.append([x.occurrence for x in item])

    # caso speciale 'se se ne occupa'
    to_be_deleted = []
    for lista in indexes:
        for i, index in enumerate(lista):
            if tags[index].occurrence == "se" and tags[index + 1].occurrence == "se":
                to_be_deleted.append(index)
                break
    for tbd in to_be_deleted:
        for i, item in enumerate(zip(indexes, strings)):
            j, w = item
            if tbd in j:
                tags[j[0]].gender = tags[j[0]].person = tags[j[0]].number = "—"
                del j[0]
                del w[0]
    return strings, indexes
