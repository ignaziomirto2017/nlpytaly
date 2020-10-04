from typing import List

from ..crea_blocchi import increment
from ...Tag import Tag

determinanti = ["DET:def", "DET:indef", "PRO:demo", "PRO:indef", "DET:part"]
# pi = preposizioni improprie
pi = [
    "accanto",
    "addosso",
    "contro",
    "dietro",
    "dinanzi",
    "dopo",
    "sotto",
]


def find_det_NP(tags: List[Tag], all_tags: List[Tag]):
    indexes: List[List[int]] = list()
    for i in range(len(tags)):
        lt = len(tags)
        if (
            tags[i].pos in determinanti
            and not tags[i - 1].is_preposition()
            and tags[i - 1].occorrenza not in pi
        ):
            indexes.append([tags[i].index])  # il ...
            if (
                i + 2 < lt
                and tags[i + 1].pos in ["ADJ", "VER:ppre"]
                and "infi" in tags[i + 2].pos
            ):
                # ... bel declinare
                indexes[-1].append(tags[i + 1].index)
                indexes[-1].append(tags[i + 2].index)
            elif i + 2 < lt and tags[i + 1].pos in ["ADJ", "VER:ppre"]:
                if tags[i + 2].pos in ["NOM", "NPR"]:  # un grande colpo; il bel Mario
                    indexes[-1].append(tags[i + 1].index)
                    indexes[-1].append(tags[i + 2].index)
                else:  # il primo, il biondo
                    indexes[-1].append(tags[i + 1].index)
            elif (
                i + 2 < lt
                and tags[i + 1].occorrenza in ["più", "meno"]
                and tags[i + 2].pos in ["ADJ", "VER:ppre"]
            ):
                # ... più bello, il meno accomodante
                indexes[-1].append(tags[i + 1].index)
                indexes[-1].append(tags[i + 2].index)
            elif i + 1 < lt and "infi" in tags[i + 1].pos:
                # ... declinare
                indexes[-1].append(tags[i + 1].index)
            elif i + 1 < lt and tags[i + 1].occorrenza == "tutto":  # settembre 19
                # il tutto
                indexes[-1].append(tags[i + 1].index)
            elif (
                i + 2 < lt
                and tags[i + 1].pos in ["ADJ", "NUM"]
                and tags[i + 2].pos != "NOM"
            ):
                # ... simpatico (inteso come sostantivo)
                indexes[-1].append(tags[i + 1].index)
            elif i + 1 < lt and tags[i + 1].lemma in ["quale", "quali"]:
                # ... quale
                indexes[-1].append(tags[i + 1].index)
            elif i + 2 < lt and tags[i + 1].pos in ["NOM"]:
                if tags[i + 2].pos in [
                    "NOM",
                    "NPR",
                    "ADJ",
                    "VER:pper",
                ]:  # il marito Oliver; 'VER:pper' aggiunto 28/09/2019
                    indexes[-1].append(
                        tags[i + 1].index
                    )  # le audizioni pubblicate/le audizioni pubbliche
                    indexes[-1].append(tags[i + 2].index)
                else:  # il primo, il biondo
                    indexes[-1].append(tags[i + 1].index)
            # l'else seguente sembra non aver rilievo (28/09/2019)
            else:
                if (
                    i + 1 < lt
                    and not tags[i + 1].is_adverb()
                    and not tags[i + 1].is_verb()
                ):
                    count = 1
                    while (
                        i + count < lt
                        and "NOM" not in tags[i + count].pos
                        and "NPR" not in tags[i + count].pos
                    ):
                        indexes[-1].append(tags[i + count].index)
                        count += 1
                    if i + count < lt:
                        indexes[-1].append(tags[i + count].index)
                    count += 1
                    if i + count < lt and tags[i + count].is_adjective():
                        indexes[-1].append(tags[i + count].index)

    indexes = list(map(lambda x: tuple(x), indexes))
    for tupla in indexes:
        for i in tupla:
            all_tags[i].is_candidate = True

    if len(indexes) > 1:
        increment(all_tags, indexes[-1][0])
    return indexes
