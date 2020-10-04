from typing import List

from .common_data import *
from ..data.clitici import clitici_riflessivi, clitici


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
        is_verb,
    )

    def __init__(self, occorrenza, pos, lemma, note="-"):
        self._occorrenza: str = occorrenza
        self.pos: str = pos
        self._lemma: str = lemma

        self.note: str = note

        self.genere = "-"
        self.numero = "-"
        self.persona = "-"

        self.index = -1
        self.block = -1

        self.all_tags: List["Tag"] = list()
        self._diathesis = None
        self.has_subject = None
        self._is_impersonal = None
        self._cov_sub = ""
        self._ruolo_sintattico = None
        self.is_verbo_flesso = None
        self.is_candidate = None
        self.is_proclisi = None
        self.is_fare_causativo = False

    def __eq__(self, other):
        return (
            self.occ == other.occ
            and self.pos == other.pos
            and self.lemma == other.lemma
            and self.genere == other.genere
            and self.numero == other.numero
            and self.persona == other.persona
        )

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
        self._cov_sub = cov_sub

    def get_cov_sub(self):
        assert self.is_verb()
        if self_block := self.get_same_block_tags():
            return self_block[0].cov_sub

    @property
    def ruolo_sintattico(self):
        return self._ruolo_sintattico

    @ruolo_sintattico.setter
    def ruolo_sintattico(self, role: str):
        assert role in [
            "SOGG",
            "OD",
            "PN",
            "SOGG|OD",
        ]
        self._ruolo_sintattico = role

    @property
    def diathesis(self):
        return self._diathesis

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
    def occorrenza(self):
        return self._occorrenza.lower()

    @property
    def occ(self):
        return self.occorrenza

    @occorrenza.setter
    def occorrenza(self, occorrenza):
        self._occorrenza = occorrenza

    @property
    def lemma(self):
        return self._lemma.lower()

    @lemma.setter
    def lemma(self, lemma):
        self._lemma = lemma

    def __str__(self):
        return (
            f"{self.index} {self.block} "
            f"{self.occorrenza} {self.pos} {self.lemma} "
            f"{self.genere} {self.numero} "
            f"{self.persona} {self.note}"
        )

    def __repr__(self):
        return str(self)

    def is_singular(self) -> bool:
        return "s" in self.numero

    def is_plural(self) -> bool:
        return "p" in self.numero

    def match_pn(self, other: "Tag") -> bool:
        return self.match_p(other) and self.match_n(other)

    def match_gn(self, other: "Tag") -> bool:
        return self.match_g(other) and self.match_n(other)

    def match_p(self, other: "Tag") -> bool:
        self_p = self.persona.split("|")
        other_p = other.persona.split("|")
        return any([x in other_p for x in self_p])

    def match_n(self, other: "Tag") -> bool:
        self_n = self.numero.split("|")
        other_n = other.numero.split("|")
        return any([x in other_n for x in self_n])

    def match_g(self, other: "Tag") -> bool:
        self_g = self.genere.split("|")
        other_g = other.genere.split("|")
        return any([x in other_g for x in self_g])

    def is_clit_refl(self) -> bool:
        return self.occorrenza in clitici_riflessivi

    def is_clit(self) -> bool:
        return self.occorrenza in clitici

    def copy(self) -> "Tag":
        return Tag(self.occorrenza, self.pos, self.lemma)

    def is_aux(self) -> bool:
        return "AUX" in self.note

    def is_pred(self) -> bool:
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

    def any_occurrences_in_block(self, words: List[str]):
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
    def get_same_block_indexes(self) -> tuple:
        return tuple([tmp.index for tmp in self.get_same_block_tags()])

    def get_prev_block_indexes(self):
        return tuple([tmp.index for tmp in self.get_prev_block_tags()])

    def get_tags_by_indexes(self, step=1, number_of_tags=1):
        result = []
        for i in range(self.index - step, self.index - step + number_of_tags):
            if i < self.index:
                result += [tmp for tmp in self.all_tags if tmp.index == i]
        return result

    def get_same_block_occurrences(self):
        return [x.occorrenza for x in self.get_same_block_tags()]

    def get_same_block_pos(self):
        return [x.pos for x in self.get_same_block_tags()]

    def get_same_block_lemmas(self):
        return [x.lemma for x in self.get_same_block_tags()]

    def get_next_block_lemmas(self):
        return [x.lemma for x in self.get_next_block_tags()]

    def get_next_block_occurrences(self, step=1, number_of_blocks=1):
        return [
            tmp.occorrenza
            for tmp in self.get_next_block_tags(
                step=step, number_of_blocks=number_of_blocks
            )
        ]

    def get_prev_block_occurrences(self, step=1, number_of_blocks=1):
        return [
            tmp.occorrenza
            for tmp in self.get_prev_block_tags(
                step=step, number_of_blocks=number_of_blocks
            )
        ]

    def is_in_SV_block(self) -> bool:
        return any(t.is_inflected_verb() for t in self.get_same_block_tags())

    def is_in_SN_block(self) -> bool:
        sb = self.get_same_block_tags()
        first_tag = sb[0]
        return any(
            [first_tag.is_article(), "NPR" in first_tag.pos, "NOM" in first_tag.pos,]
        )

    def get_block_clitici(self) -> List["Tag"]:
        if not self.is_in_SV_block():
            raise ValueError
        res = []
        for t in self.get_same_block_tags():
            if t.is_clit():
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
            "gn": f"{self.genere} {self.numero}",
            "persona": f"{self.persona}",
            "index": self.index,
            "block": self.block,
            "note": self.note,
            "cov_sub": self.cov_sub,
        }
