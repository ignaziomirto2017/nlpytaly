from typing import List

from ..create_blocks import increment
from ...Tag import Tag
from ...data.kinship_names import kinship_names

determinanti = ["DET:def", "DET:indef", "PRO:demo", "PRO:indef", "DET:part"]
improper_prepositions = [
    "accanto",
    "addosso",
    "contro",
    "dietro",
    "dinanzi",
    "dopo",
    "sotto",
    "vicino",
]


def mark_as_candidate(result: List[List[int]], all_tags: List[Tag]):
    for t in result:
        for i in t:
            all_tags[i]._is_sub_obj_candidate = True


def search_det_np(tags: List[Tag], all_tags: List[Tag]) -> List[List[int]]:
    indexes: List[List[int]] = list()
    for i in range(len(tags)):
        lt = len(tags)
        if (
            tags[i].pos in determinanti
            and not tags[i - 1].is_preposition()
            and tags[i - 1].occurrence not in improper_prepositions
        ):
            indexes.append([tags[i].index])  # il ...
            if (
                i + 2 < lt
                and tags[i + 1].pos in ["ADJ", "VER:pper"]
                and "infi" in tags[i + 2].pos
            ):
                # ... bel declinare
                indexes[-1].append(tags[i + 1].index)
                indexes[-1].append(tags[i + 2].index)
            elif i + 2 < lt and tags[i + 1].pos in ["ADJ", "VER:pper"]:
                if tags[i + 2].pos in [
                    "NOM",
                    "NPR",
                ]:  # un grande colpo; il bel Mario
                    indexes[-1].append(tags[i + 1].index)
                    indexes[-1].append(tags[i + 2].index)
                else:  # il primo, il biondo
                    indexes[-1].append(tags[i + 1].index)
            elif (
                i + 2 < lt
                and tags[i + 1].occurrence in ["più", "meno"]
                and tags[i + 2].pos in ["ADJ", "VER:pper"]
            ):
                # ... più bello, il meno accomodante
                indexes[-1].append(tags[i + 1].index)
                indexes[-1].append(tags[i + 2].index)
            elif i + 1 < lt and "infi" in tags[i + 1].pos:
                # ... declinare
                indexes[-1].append(tags[i + 1].index)
            elif i + 1 < lt and tags[i + 1].occurrence == "tutto":  # settembre 19
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
                    if i + 3 < lt and tags[i + 3].pos == "VER:pper":
                        indexes[-1].append(tags[i + 3].index)

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

    indexes = list(map(lambda x: list(x), indexes))
    mark_as_candidate(indexes, all_tags)

    if len(indexes) > 1:
        increment(all_tags, indexes[-1][0])
    return indexes


# Mario mangia patate, Mario mangia belle patate
def find_bare_plural_noun(all_tags: List[Tag], done) -> List[List[int]]:
    result: List[List[int]] = []
    for i, t in enumerate(all_tags):
        if t.is_noun() and t.is_plural():
            if i >= 1 and all_tags[t.index - 1].is_verb():
                if t.index not in done:
                    result.append(
                        [t.index,]
                    )
                    done.add(t.index)
            elif (
                i >= 2
                and all_tags[t.index - 2].is_verb()
                and (
                    all_tags[t.index - 1].is_adjective()
                    or all_tags[t.index - 1].is_pro_poss()
                )
            ):
                if t.index not in done:
                    result.append(
                        [t.index - 1, t.index,]
                    )
                    done.add(t.index)
    mark_as_candidate(result, all_tags)
    return result


# Mio zio parla, Vedo mio cugino
def nomi_di_parentela(all_tags: List[Tag], done):
    result: List[List[int]] = []
    for i, t in enumerate(all_tags):
        if t.is_pro_poss():
            if t.next() and t.next().occ in kinship_names:
                if t.index not in done:
                    result.append([t.index, t.next().index])
                    done.add(t.index)
    mark_as_candidate(result, all_tags)
    return result
