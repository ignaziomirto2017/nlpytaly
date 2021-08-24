import re
import time
from typing import Dict, Tuple, List, Union

from .Tag import Tag
from .data.places import places
from .data.verbs.weather_verbs import weather_verbs
from .operations.create_blocks import fix


def line_to_clean_lines(line: str):
    r = "([.;:!?])"
    lines = re.split(r, line)
    tmp = []
    for i in range(0, len(lines) - 1, 2):
        tmp.append(lines[i] + lines[i + 1])
    lines = tmp
    lines = list(map(lambda riga: riga.strip(), lines))
    return lines


def get_candidate(candidates: List[List[Tuple[str, List[int]]]], index: int):
    for item in candidates:
        for tupla in item:
            if index in tupla:
                return tuple(tupla)
    return tuple()


def get_subj_obj_for_tag(t: Tag, ruoli_sintattici_result: Dict):
    # sogg, od, pn, sogg|od
    result = [None, None, None, None]
    v_block_indexes = t.get_same_block_indexes()
    for k, v in ruoli_sintattici_result.items():
        if v[1] == v_block_indexes:
            if v[0] == "SOGG":
                result[0] = k
            elif v[0] == "OD":
                result[1] = k
            elif v[0] == "PN":
                result[2] = k
            elif v[0] == "SOGG|OD":
                result[3] = k
    return result


def get_subj_obj_tags_for_tag(
    t: Tag, tags: List[Tag], ruoli_sintattici_result: Dict
) -> List[Tag]:
    result = get_subj_obj_for_tag(t, ruoli_sintattici_result)
    for i, item in enumerate(result):
        item: Tuple[int]
        if item:
            result[i] = [tags[x] for x in item]
    return result


def get_subj_obj_occurrences_for_tag(
    t: Tag, tags: List[Tag], ruoli_sintattici_result: Dict, wrap="'"
) -> List[str]:
    result = get_subj_obj_for_tag(t, ruoli_sintattici_result)
    for i, item in enumerate(result):
        item: Tuple[int]
        if item:
            result[i] = wrap + " ".join(tags[x].occurrence for x in item).upper() + wrap
    return result


def search_x_phrase(tags, to_be_searched) -> Union[None, List[Tag]]:
    for i, tag in enumerate(tags):
        if tag.lemma in to_be_searched:
            x_phrase_si: List[Tag] = [
                x
                for x in tags[i:]
                if "NPR" in x.pos
                or "NOM" in x.pos
                or "PRE:det" in x.pos
                or "PRO:demo" in x.pos
                or "PRO:pers" in x.pos
                or "PRO:poss" in x.pos
                or "DET:indef" in x.pos
                or "PRE" in x.pos
                or "ADJ" in x.pos
            ]
            # teniamo solo la prima preposizione
            # per evitare ad es. "alla sorella da Maria"
            prepositions = 0
            last_prep_index = -1
            for j, item in enumerate(x_phrase_si):
                if "PRE" in item.pos:
                    prepositions += 1
                    last_prep_index = j
            if prepositions >= 2:
                x_phrase_si = x_phrase_si[0:last_prep_index]

            if x_phrase_si:
                block = x_phrase_si[0].block
                x_phrase_si = [x for x in x_phrase_si if x.block == block]

            if x_phrase_si[0].occ in {"da", "a"}:
                x_phrase_si = x_phrase_si[1:]
            else:
                suffixes = {
                    "'": "l'",
                    "l": "il",
                    "lo": "lo",
                    "la": "la",
                    "gli": "gli",
                    "i": "i",
                    "le": "le",
                }
                tmp = x_phrase_si[1:]
                for k, v in suffixes.items():
                    if x_phrase_si[0].occ.endswith(k):
                        x_phrase_si = [Tag(v, "DET:def", "il")] + tmp
                        break

            if to_be_searched == ["a", "al"] and x_phrase_si:
                if x_phrase_si[-1]._occurrence in places:
                    x_phrase_si = None

            return x_phrase_si
    else:
        x_phrase_si = None

    return x_phrase_si


def search_a_phrase(tags) -> List[Tag]:
    return search_x_phrase(tags, to_be_searched=["a", "al"])


def search_da_phrase(tags) -> List[Tag]:
    return search_x_phrase(tags, to_be_searched=["da", "dal"])


def increment_blocks(tags, start, end):  # inclusi
    assert start <= end < len(tags)
    first = start == 0
    if not first:
        for i in range(start, end + 1):
            tags[i].block += 1
            fix(tags)

    for i in range(end + 1, len(tags)):
        tags[i].block += 1 if first else 2
        fix(tags)


def save_sentence(sentence: str):
    with open("history.txt", "a") as f:
        f.write(f"{sentence} - {time.strftime('%Y-%m-%d %H:%M')}\n")


def get_diatheses(tags: List[Tag]):
    all_items = []
    blocks_done = set()
    for t in tags:
        if t.block not in blocks_done:
            block = t.get_same_block_tags()
            words = " ".join(tmp.occurrence for tmp in block if tmp.pos != "ADV")
            if any(k.is_verb() for k in block):
                if t.diathesis == "ACTIVE":
                    all_items.append((words, 0))
                elif t.diathesis == "PASSIVE":
                    all_items.append((words, 1))
                elif t.diathesis == "MIDDLE_PR":
                    all_items.append((words, 2))
                elif t.diathesis == "MIDDLE_MR":
                    all_items.append((words, 3))
            blocks_done.add(t.block)
    return all_items


def find_covert_subjects(ov, result, tags, verbs_with_overt_subject):
    for t in tags:
        if t.is_inflected_verb():
            verbal_block_indexes = t.get_same_block_indexes()
            verbal_block_lemmas = t.get_same_block_lemmas()
            if t.person == "1st" and t.number == "s":
                if verbal_block_indexes not in verbs_with_overt_subject:
                    t.cov_sub = 1
                    result.append(
                        f"The covert subject of '{ov(verbal_block_indexes)}'  is 'IO'."
                    )
            elif t.person == "2nd" and t.number == "s":
                if verbal_block_indexes not in verbs_with_overt_subject:
                    t.cov_sub = 2
                    result.append(
                        f"The covert subject of '{ov(verbal_block_indexes)}'  is 'TU'."
                    )
            elif t.person == "1st" and t.number == "p":
                if verbal_block_indexes not in verbs_with_overt_subject:
                    t.cov_sub = 4
                    result.append(
                        f"The covert subject of '{ov(verbal_block_indexes)}'  is 'NOI'."
                    )
            elif t.person == "2nd" and t.number == "p":
                if verbal_block_indexes not in verbs_with_overt_subject:
                    t.cov_sub = 5
                    result.append(
                        f"The covert subject of '{ov(verbal_block_indexes)}'  is 'VOI'."
                    )
            elif t.person == "3rd" and t.number == "s":
                if (
                    any(x in weather_verbs for x in verbal_block_lemmas)
                    or t.is_impersonal()
                ):
                    continue
                if verbal_block_indexes not in verbs_with_overt_subject:
                    t.cov_sub = 3
                    result.append(
                        f"The covert subject of '{ov(verbal_block_indexes)}'  is 'LUI|LEI'."
                    )
            elif t.person == "3rd" and t.number == "p":
                if verbal_block_indexes not in verbs_with_overt_subject:
                    t.cov_sub = 6
                    result.append(
                        f"The covert subject of '{ov(verbal_block_indexes)}'  is 'LORO'."
                    )


def wording_syntactic_roles(ruoli_sintattici_result: dict, tags: List[Tag]):
    def ov(t: tuple):  # da tupla a occorrenza, per i verbs (ov = occorrenze verbs)
        return " ".join(
            tags[x].occurrence.upper() for x in t if tags[x].pos not in ["ADV", "PRE"]
        )

    def on(t: tuple):  # da tupla a occorrenza, per i nomi (on = occorrenze nomi)
        return " ".join(tags[x].occurrence.upper() for x in t)

    result: List[str] = []
    verbs_with_overt_subject = set()
    for k, v in sorted(ruoli_sintattici_result.items(), key=lambda x: x[1][1][0]):
        (
            ruolo,
            destinatario,
        ) = v  # ruolo = funzione sintattica, destinatario = sintagma abbinato
        if ruolo == "SOGG|OD":
            result.append(
                f"The subject\\direct object of  '{ov(destinatario)}'  is '{on(k)}'."
            )
            verbs_with_overt_subject.add(destinatario)  # destinatario = verbo
        elif "SOGG" in ruolo:
            result.append(f"The subject of  '{ov(destinatario)}'  is '{on(k)}'.")
            verbs_with_overt_subject.add(destinatario)  # destinatario = verbo
        elif "OD" in ruolo:
            result.append(f"The direct object of  '{ov(destinatario)}'  is  '{on(k)}'.")
        elif "PN" in ruolo:
            result.append(
                f"'{ov(destinatario)}' e '{on(k)}' formano un predicato nominale."
            )
    find_covert_subjects(ov, result, tags, verbs_with_overt_subject)

    return result


def mark_tag(t: Tag, k: str, v) -> None:
    setattr(t, k, v)


def get_attr(t, k):
    return getattr(t, k, None)
