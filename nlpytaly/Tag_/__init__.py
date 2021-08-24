from typing import List, Tuple, Iterable

from .common_data import *
from ..data.clitics import reflexive_clitics, clitics


class Tag(object):
    from .set_pgn_methods import set_g, set_gn, set_n, set_p, set_pn
    from .is_pos_methods import (
        is_adjective,
        is_adverb,
        is_article,
        is_gerund,
        is_infinitive,
        is_inflected_verb,
        is_noun,
        is_past_participle,
        is_preposition,
        is_pro_pers,
        is_pro_poss,
        is_verb,
        is_npr,
    )

    def __init__(self, occurrence, pos, lemma, note="-"):
        self._occurrence: str = occurrence
        self.pos: str = pos
        self._lemma: str = lemma

        self.note: str = note

        self.gender = "-"
        self.number = "-"
        self.person = "-"

        self.index = -1
        self.block = -1

        self.all_tags: List["Tag"] = list()
        self._diathesis = None
        self.has_subject = None
        self._is_impersonal = None
        self._cov_sub = ""
        self._syntactic_role = None
        self._is_inflected_verb = None
        self._is_sub_obj_candidate = None
        self.is_proclisis = None
        self._is_causative_fare = False

        # verbal block expressed as verb: Tuple[int]
        #   max number of sem roles permitted per tag per verbal block
        self.max_no_sr = {}
        # current number of sem roles per tag per verbal block
        self.cur_no_sr = {}

    def __eq__(self, other):
        return (
            self.occ == other.occ
            and self.pos == other.pos
            and self.lemma == other.lemma
            and self.gender == other.gender
            and self.number == other.number
            and self.person == other.person
        )

    def sem_role_allowed(self, verb: Tuple[int]):
        return self.cur_no_sr.get(verb, 0) < self.max_no_sr.get(verb, 2)

    def sem_role_inc(self, verb: Tuple[int]):
        self.cur_no_sr[verb] = self.cur_no_sr.get(verb, 0) + 1

    def sem_role_set_max(self, m: int, verb: Tuple[int]):
        self.max_no_sr[verb] = m

    @property
    def cov_sub(self):
        d = {
            "": "",
            1: "IO",
            2: "TU",
            3: "LUI|LEI",
            4: "NOI",
            5: "VOI",
            6: "LORO",
        }
        return d[self._cov_sub]

    @cov_sub.setter
    def cov_sub(self, cov_sub: int):
        assert cov_sub in list(range(1, 7))
        for x in self.get_same_block_tags():
            x._cov_sub = cov_sub

    def get_cov_sub(self):
        assert self.is_verb()
        if self_block := self.get_same_block_tags():
            return self_block[0].cov_sub

    @property
    def syntactic_role(self):
        return self._syntactic_role

    @syntactic_role.setter
    def syntactic_role(self, role: str):
        assert role in [
            "SOGG",
            "OD",
            "PN",
            "SOGG|OD",
        ]
        self._syntactic_role = role

    @property
    def diathesis(self):
        return self._diathesis

    def has_diathesis(self):
        return self._diathesis is not None

    @diathesis.setter
    def diathesis(self, diathesis: str):
        assert diathesis in [
            "ACTIVE",
            "PASSIVE",
            "MIDDLE_PR",  # plus reflexive
            "MIDDLE_MR",  # minus reflexive
        ]
        self._diathesis = diathesis

    @property
    def occurrence(self):
        return self._occurrence.lower()

    @property
    def is_causative_fare(self):
        return any(x._is_causative_fare for x in self.get_same_block_tags())

    @is_causative_fare.setter
    def is_causative_fare(self, causative_fare):
        for t in self.get_same_block_tags():
            t: Tag
            t._is_causative_fare = causative_fare

    @property
    def occ(self):
        return self.occurrence

    @occurrence.setter
    def occurrence(self, occurrence):
        self._occurrence = occurrence

    @property
    def lemma(self):
        return self._lemma.lower()

    @lemma.setter
    def lemma(self, lemma):
        self._lemma = lemma

    def __str__(self):
        return (
            f"{self.index} {self.block} "
            f"{self.occurrence} {self.pos} {self.lemma} "
            f"{self.gender} {self.number} "
            f"{self.person} {self.note}"
        )

    def __repr__(self):
        return str(self)

    def distance(self, other) -> int:
        return abs(self.index - other.index)

    def is_singular(self) -> bool:
        return "s" in self.number

    def is_plural(self) -> bool:
        return "p" in self.number

    def match_pn(self, other: "Tag") -> bool:
        return self.match_p(other) and self.match_n(other)

    def match_gn(self, other: "Tag") -> bool:
        return self.match_g(other) and self.match_n(other)

    def match_p(self, other: "Tag") -> bool:
        self_p = self.person.split("|")
        other_p = other.person.split("|")
        return any([x in other_p for x in self_p])

    def match_n(self, other: "Tag") -> bool:
        self_n = self.number.split("|")
        other_n = other.number.split("|")
        return any([x in other_n for x in self_n])

    def match_g(self, other: "Tag") -> bool:
        self_g = self.gender.split("|")
        other_g = other.gender.split("|")
        return any([x in other_g for x in self_g])

    def is_reflexive_clitic(self) -> bool:
        return self.occurrence in reflexive_clitics

    def is_clitic(self) -> bool:
        return self.occurrence in clitics

    def copy(self) -> "Tag":
        return Tag(self.occurrence, self.pos, self.lemma)

    def is_aux(self) -> bool:
        return "AUX" in self.note

    def is_modal(self) -> bool:
        return self.lemma in {"dovere", "potere"}

    def is_predicative(self) -> bool:
        return "PRED" in self.note

    def is_main_verb(self) -> bool:
        return "Main verb" in self.note

    # diathesis
    def is_active(self) -> bool:
        return self.diathesis == "ACTIVE"

    def is_passive(self) -> bool:
        return self.diathesis == "PASSIVE"

    def is_middle_pr(self) -> bool:
        return self.diathesis == "MIDDLE_PR"

    def is_middle_mr(self) -> bool:
        return self.diathesis == "MIDDLE_MR"

    def is_middle(self) -> bool:
        return self.is_middle_pr() or self.is_middle_mr()

    def get_same_block_tags(self) -> List["Tag"]:
        return [tmp for tmp in self.all_tags if tmp.block == self.block]

    def get_prev_block_tags(self, step=1, number_of_blocks=1) -> List["Tag"]:
        result = []
        for i in range(self.block - step, self.block - step + number_of_blocks):
            if i < self.block:
                result += [tmp for tmp in self.all_tags if tmp.block == i]
        return result

    def get_next_block_tags(self, step=1, number_of_blocks=1) -> List["Tag"]:
        result = []
        for i in range(self.block + step, self.block + step + number_of_blocks):
            result += [tmp for tmp in self.all_tags if tmp.block == i]
        return result

    def is_same_block(self, other: "Tag") -> bool:
        return self.block == other.block

    def is_prev_block(self, other: "Tag") -> bool:
        return self.block == other.block - 1

    def is_next_block(self, other: "Tag") -> bool:
        return self.block == other.block + 1

    def is_occurrence_in_block(self, word: str):
        return word in self.get_same_block_occurrences()

    def any_occurrences_in_block(self, words: Iterable[str]):
        for w in words:
            if self.is_occurrence_in_block(w):
                return True
        return False

    def is_lemma_in_block(self, word: str):
        return word in self.get_same_block_lemmas()

    def any_lemmas_in_block(self, words: List[str]):
        for w in words:
            if self.is_lemma_in_block(w):
                return True
        return False

    # indexes
    def get_same_block_indexes(self) -> Tuple[int]:
        return tuple([tmp.index for tmp in self.get_same_block_tags()])

    def get_prev_block_indexes(self):
        return tuple([tmp.index for tmp in self.get_prev_block_tags()])

    def get_tags_by_indexes(self, step=1, number_of_tags=1):
        result = []
        for i in range(self.index - step, self.index - step + number_of_tags):
            if i < self.index:
                result += [tmp for tmp in self.all_tags if tmp.index == i]
        return result

    def get_tags_by_block(self, block: int):
        result: List[Tag] = []
        for t in self.all_tags:
            if t.block == block:
                result.append(t)
        return result

    def get_same_block_occurrences(self):
        return [x.occurrence for x in self.get_same_block_tags()]

    def get_same_block_pos(self) -> List[str]:
        return [x.pos for x in self.get_same_block_tags()]

    def get_same_block_lemmas(self) -> List[str]:
        return [x.lemma for x in self.get_same_block_tags()]

    def get_next_block_lemmas(self) -> List[str]:
        return [x.lemma for x in self.get_next_block_tags()]

    def get_next_block_occurrences(self, step=1, number_of_blocks=1) -> List[str]:
        return [
            tmp.occurrence
            for tmp in self.get_next_block_tags(
                step=step, number_of_blocks=number_of_blocks
            )
        ]

    def get_prev_block_occurrences(self, step=1, number_of_blocks=1) -> List[str]:
        return [
            tmp.occurrence
            for tmp in self.get_prev_block_tags(
                step=step, number_of_blocks=number_of_blocks
            )
        ]

    def get_adjacent_candidates(
        self, candidates: List[List[List[int]]]
    ) -> List[List[int]]:
        if not self.is_in_SV_block():
            return []
        result: List[List[int]] = []
        if self.block > 0:
            if prev_tags := self.get_tags_by_block(self.block - 1):
                prev_indexes = list(prev_tags[0].get_same_block_indexes())
                for block in candidates:
                    if prev_indexes in block:
                        result.append(prev_indexes)
        if self.block < self.all_tags[-1].block:
            if next_tags := self.get_tags_by_block(self.block + 1):
                next_indexes = list(next_tags[0].get_same_block_indexes())
                for block in candidates:
                    if next_indexes in block:
                        result.append(next_indexes)

        return result

    def is_in_SV_block(self) -> bool:
        return any(t.is_inflected_verb() for t in self.get_same_block_tags())

    def is_in_SN_block(self) -> bool:
        sb = self.get_same_block_tags()
        first_tag = sb[0]
        res = [
            first_tag.is_article(),
            "NPR" in first_tag.pos,
            "NOM" in first_tag.pos,
        ]
        return any(res)

    def get_block_clitics(self) -> List["Tag"]:
        if not self.is_in_SV_block():
            raise ValueError
        res = []
        for t in self.get_same_block_tags():
            if t.is_clitic():
                res.append(t)
        return res

    def set_impersonal(self):
        if not self.is_in_SV_block():
            raise ValueError
        for t in self.get_same_block_tags():
            t._is_impersonal = True

    def is_impersonal(self):
        return all(t._is_impersonal for t in self.get_same_block_tags())

    def to_dict(self):
        return {
            "occurrence": self.occ,
            "pos": self.pos,
            "lemma": self.lemma,
            "gn": f"{self.gender} {self.number}",
            "persona": f"{self.person}",
            "index": self.index,
            "block": self.block,
            "note": self.note,
            "cov_sub": self.cov_sub,
        }

    def next(self) -> "Tag":
        index = self.index
        if index + 1 < len(self.all_tags):
            return self.all_tags[index + 1]
        return None

    def prev(self) -> "Tag":
        index = self.index
        if index - 1 >= 0:
            return self.all_tags[index - 1]
        return None

    def is_marked(self):
        return any(x.startswith("PRED") for x in dir(self))
