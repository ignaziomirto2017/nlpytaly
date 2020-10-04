from typing import List, Tuple

from ..Tag import Tag
from ..data.clitici import clitici, clitici_a_meno_uno


def trova_proclisi(tags: List[Tag]) -> Tuple[List[List[str]], List[List[int]]]:
    lista_proclisi: List[List[Tag]] = []
    for i in range(len(tags)):
        clitic: List[Tag] = []
        t = tags[i]
        if t.is_inflected_verb():
            if (
                i >= 4
                and tags[i - 4].lemma == "non"
                and tags[i - 3].occorrenza.lower() in clitici
                and tags[i - 2].occorrenza.lower() in clitici
                and tags[i - 1].occorrenza.lower() in clitici_a_meno_uno
            ):
                clitic.append(tags[i - 4])
                clitic.append(tags[i - 3])
                clitic.append(tags[i - 2])
                clitic.append(tags[i - 1])
            elif (
                i >= 3
                and tags[i - 3].occorrenza in clitici
                and tags[i - 2].occorrenza in clitici
                and tags[i - 1].occorrenza in clitici_a_meno_uno
            ):
                clitic.append(tags[i - 3])
                clitic.append(tags[i - 2])
                clitic.append(tags[i - 1])
            elif (
                i >= 3
                and tags[i - 3].lemma == "non"
                and tags[i - 2].occorrenza
                and tags[i - 1].occorrenza in clitici_a_meno_uno
            ):
                clitic.append(tags[i - 3])
                clitic.append(tags[i - 2])
                clitic.append(tags[i - 1])
            elif (
                i >= 2
                and tags[i - 2].lemma == "non"
                and tags[i - 1].occorrenza in clitici
            ):
                clitic.append(tags[i - 2])
                clitic.append(tags[i - 1])
            elif (
                i >= 2
                and tags[i - 2].occorrenza in clitici
                and tags[i - 1].occorrenza in clitici
            ):
                clitic.append(tags[i - 2])
                clitic.append(tags[i - 1])

            elif i >= 1 and tags[i - 1].occorrenza in clitici_a_meno_uno:
                clitic.append(tags[i - 1])

            for item in clitic:
                item.is_proclisi = True
            lista_proclisi.append(clitic[:])
    indexes = []
    strings = []
    for item in lista_proclisi:
        indexes.append([x.index for x in item])
        strings.append([x.occorrenza for x in item])

    # caso speciale 'se se ne occupa'
    to_be_deleted = []
    for lista in indexes:
        for i, index in enumerate(lista):
            if tags[index].occorrenza == "se" and tags[index + 1].occorrenza == "se":
                to_be_deleted.append(index)
                break
    for tbd in to_be_deleted:
        for i, item in enumerate(zip(indexes, strings)):
            j, w = item
            if tbd in j:
                tags[j[0]].genere = tags[j[0]].persona = tags[j[0]].numero = "—"
                del j[0]
                del w[0]
    return strings, indexes
