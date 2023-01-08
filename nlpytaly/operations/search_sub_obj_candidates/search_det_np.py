from typing import List, Set

from ...data.kinship_names import kinship_names
from ...Tag import Tag
from ..create_blocks import increment

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


def search_det_np(
    tags: List[Tag], all_tags: List[Tag], done: Set[int]
) -> List[List[int]]:
    indexes: List[List[int]] = list()
    lt = len(tags)
    for i in range(lt):
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
                if tags[i + 2].pos in ["NOM", "NPR"]:  # un grande colpo; il bel Mario
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
                    # evita: Mario ha raccontato _qualcosa a Giulio_
                    and not tags[i + 1].is_preposition()
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

    for tmp in indexes:
        for i in tmp:
            done.add(i)
    return indexes


# Mario mangia patate, Mario mangia belle patate
def find_bare_plural_noun(all_tags: List[Tag], done) -> List[List[int]]:
    result: List[List[int]] = []
    for i, t in enumerate(all_tags):
        if t.is_verb():
            tmp = [(x.pos, x.number, x.index) for x in t.get_next_block_tags()]
            match tmp:
                case [("NUM", _, i), ("NOM", "p", j), ("ADJ", "p", k), *x]:
                    # 4 simpatici amici
                    # i pos sono obbligati da un errore di TreeTagger
                    # dovrebbero essere: num, adj, nom
                    if i not in done:
                        result.append([i, j, k])
                        done.add(i)
                case [("ADJ", _, i), ("NOM", "p", j), ("ADJ", "p", k), *x]:
                    # quattro simpatici amici
                    # i pos sono obbligati da un errore di TreeTagger
                    # dovrebbero essere: adj, adj, nom
                    if i not in done:
                        result.append([i, j, k])
                        done.add(i)
                case [("NOM", "p", i), ("ADJ", "p", j), *x]:
                    # patate belle
                    if i not in done:
                        result.append([i, j])
                        done.add(i)
                case [("ADJ", "p", i), ("NOM", "p", j), *x]:
                    # belle patate
                    if i not in done:
                        result.append([i, j])
                        done.add(i)
                case [("PRO:poss", "p", i), ("NOM", "p", j), *x]:
                    # miei amici
                    if i not in done:
                        result.append([i, j])
                        done.add(i)
                case [("NOM", "p", i), *x]:
                    # amici
                    if i not in done:
                        result.append([i])
                        done.add(i)
                case [("NUM", _, i), ("NOM", "p", j), *x]:
                    # 4 amici
                    if i not in done:
                        result.append([i, j])
                        done.add(i)

    mark_as_candidate(result, all_tags)
    return result


# Mio zio parla, Vedo mio cugino
def nomi_di_parentela(all_tags: List[Tag], done):
    result: List[List[int]] = []
    for i, t in enumerate(all_tags):
        if t.is_pro_poss():
            p: Tag = t.prev()
            n: Tag = t.next()
            if n and n.occ in kinship_names:
                if p and p.is_preposition():
                    # avoid flagging "a suo cugino" as candidate
                    result.append([t.index, t.next().index])
                    continue
                if t.index not in done:
                    result.append([t.index, t.next().index])
                    done.add(t.index)
    mark_as_candidate(result, all_tags)
    return result
