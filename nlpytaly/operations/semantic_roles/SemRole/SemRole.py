import abc
from typing import List

from .utils import sanitize
from ...formations.past_part_formation import past_part_formation
from ...formations.reflexive_infinitive_formation import reflexive_infinitive_formation
from ...formations.third_person_formation import third_person_formation
from ....Tag import Tag
from ....data.verbs.class_2_verbs import class_2_verbs_si
from ....data.verbs.trivalent import trivalent_verbs
from ....operations.formations.article_selection import get_determinative_inf

ABSTRACT_SEM_ROLE = 0
ORDINARY_SEM_ROLE = 1
CAUSATIVE_SEM_ROLE = 2
DATIVE_SEM_ROLE = 3
JOB_SEM_ROLE = 4
ATE_SEM_ROLE = 5
SUPP_SEM_ROLE = 6
METTERE_PREP_SEM_ROLE = 7

pron_pers = {
    "IO": "1s",
    "ME": "1s",
    "TU": "2s",
    "TE": "2s",
    "ESSO": "3s",
    "LUI|LEI": "3s",
    "ESSA": "3s",
    "NOI": "1p",
    "VOI": "2p",
    "ESSI": "3p",
    "LORO": "3p",
}


class AbstractSemRole(metaclass=abc.ABCMeta):
    def __init__(self, f1, f2, f3):
        self.f1 = sanitize(f1)
        self.f2 = [sanitize(x) for x in f2]
        self.f3 = sanitize(f3)
        self.f4 = ABSTRACT_SEM_ROLE

        self.pronoun = False

        if f1.upper() in pron_pers:
            self.pronoun = f1
            self.f1 = pron_pers[f1.upper()]
        elif f1 == "":  # cov_sub not found
            self.f1 = "QUALCUNO\\QUALCOSA"

    def __str__(self):
        return f"{self.f1}, {self.f2}, {self.f3}"

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        res = self.f1 == other.f1 and self.f2 == other.f2 and self.f3 == other.f3
        return res

    def __hash__(self):
        return hash(str(self))

    def __lt__(self, other):
        return str(self) < str(other)


class OrdinarySemRole(AbstractSemRole):
    """
    f1: assignee
    f2: [derived] assigner (verb)
    f3: diathesis
    f4: ORDINARY_SEM_ROLE

    e.g.:
    f1 = La mamma
    f2 = mangiare
    f3 = ACTIVE
    => La mamma mangia (ha mangiato, etc) [la pasta]
    """

    def __init__(self, f1: str, f2: List[str], f3: str):
        assert f3 in ["ACTIVE", "ACTIVE_SI", "PASSIVE"]
        super().__init__(f1, f2, f3)
        if f2[0] in class_2_verbs_si:
            self.f3 = "ACTIVE_SI"
        self.f4 = ORDINARY_SEM_ROLE

    def __str__(self):
        v = self.f2[0]
        f1 = (self.pronoun if self.pronoun else self.f1).upper()
        if self.f3 == "ACTIVE":
            return f"{f1} è chi o cosa {third_person_formation(v)}"
        elif self.f3 == "ACTIVE_SI":
            return f"{f1} è chi o cosa {third_person_formation(v, include_si=True)}"
        elif self.f3 == "PASSIVE":
            return f"{f1} è chi o cosa è {past_part_formation(v)}"


class SuppSemRole(OrdinarySemRole):
    def __init__(self, f1, f2, f3):
        super().__init__(f1, f2, f3)
        self.f4 = SUPP_SEM_ROLE


class MetterePrepSemRole(OrdinarySemRole):
    def __init__(self, f1, f2, f3, non_verbal_origin: List[Tag]):
        super().__init__(f1, f2, f3)
        self.f4 = METTERE_PREP_SEM_ROLE
        self.non_verbal_origin = " ".join(x.occ for x in non_verbal_origin)


class AteSemRole(OrdinarySemRole):
    def __init__(self, f1, f2, f3, non_verbal_origin: List[str]):
        super().__init__(f1, f2, f3)
        self.f4 = ATE_SEM_ROLE
        self.non_verbal_origin = " ".join(non_verbal_origin)


class CausativeSemRole(OrdinarySemRole):
    __hash__ = AbstractSemRole.__hash__

    def __init__(self, f1, f2, f3, inf: str):
        super().__init__(f1, f2, f3)
        if inf in class_2_verbs_si:
            inf = reflexive_infinitive_formation(inf)
        self.inf = sanitize(inf)
        self.f4 = CAUSATIVE_SEM_ROLE

    def __str__(self):
        f1 = (self.pronoun if self.pronoun else self.f1).upper()
        tmp = sanitize(get_determinative_inf(self.inf).occ + " " + self.inf)
        print(self.f1, self.f2, self.f3, "--------------")
        return f"{f1} è chi o cosa determina {tmp}"

    def __eq__(self, other):
        return super().__eq__(other) and self.inf == other.inf


class JobSemRole(OrdinarySemRole):
    """
    f1: assignee
    f2: ["svolgere", "professione", mestiere_noun]
    f4: JobSemRole

    e.g.:
    f1 = Mario
    f2 = ["svolgere", "professione", "meccanico"]
    => Piero svolge il mestiere di meccanico
    """

    def __init__(self, f1: str, f3: str):
        super().__init__(f1, ["svolgere", "professione", f3], "ACTIVE")
        self.f4 = JOB_SEM_ROLE

    def __str__(self):
        if len(self.f2) > 2:
            return f"{self.f1} è chi svolge la professione di {self.f2[2]}"
        else:
            return f"{self.f1} è chi svolge una professione"


class DativeSemRole(OrdinarySemRole):
    """
    f1: assignee
    f2: verb
    f4: DATIVE_SEM_ROLE

    e.g.:
    f1 = Piero
    f2 = ["correggere"]
    => Piero è a chi si corregge [qualcosa ...]
    """

    def __init__(self, f1, f2):
        super().__init__(f1, f2, "ACTIVE_SI")
        self.f4 = DATIVE_SEM_ROLE

    def __str__(self):
        v = self.f2[0].lower()
        vc = third_person_formation(v, include_si=True)
        if v in trivalent_verbs:
            return f"{self.f1} è a chi {vc} qualcosa"
        else:
            return f"{self.f1} è a chi {vc}"
