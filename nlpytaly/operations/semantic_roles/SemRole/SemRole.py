import abc
import hashlib
from typing import List

from ....data.verbs.class_2_verbs import class_2_verbs_si, two_place_predicate2
from ....data.verbs.trivalent import trivalent_verbs
from ....operations.formations.article_selection import get_determinative_inf
from ....Tag import Tag
from ...formations.past_part_formation import past_part_formation
from ...formations.reflexive_infinitive_formation import reflexive_infinitive_formation
from ...formations.third_person_formation import third_person_formation
from .consts import (
    ABSTRACT_SEM_ROLE,
    ACTV,
    ACTV_S,
    AMBIGUOUS_SEM_ROLE,
    ATE_SEM_ROLE,
    CAUSATIVE_SEM_ROLE,
    DATIVE_SEM_ROLE,
    JOB_SEM_ROLE,
    METTERE_PREP_SEM_ROLE,
    ORDINARY_SEM_ROLE,
    SUPP_SEM_ROLE,
)
from .utils import sanitize

# person, number, gender
_pron_pers = {
    "IO": "1S",
    "ME": "1S",
    "TU": "2S",
    "TE": "2S",
    "ESSO": "3SM",
    "LUI|LEI": "3S",
    "LUI": "3SM",
    "LEI": "3SF",
    "ESSA": "3SF",
    "NOI": "1P",
    "VOI": "2P",
    "ESSI": "3PM",
    "ESSE": "3PF",
    "LORO": "3P",
}

_clitics_do = {
    "MI": "1S",
    "CI": "1P",
    "TI": "2S",
    "VI": "2P",
    "LO": "3SM",
    "LA": "3SF",
    "L'": "3S",
    "LE": "3PF",
    "LI": "3PM",
}

_clitics_io = {
    "MI": "1S",
    "CI": "1P",
    "TI": "2S",
    "VI": "2P",
    "GLI": "3",
    "LE": "3SF",
    # for testing
    # see entailment_02_test:test2
    "1S": "1S",
    "1P": "1P",
    "2S": "2S",
    "2P": "2P",
    "3": "3",
    "3SF": "3SF",
}

_feature_pronoun = {
    "1S": "ME",
    "2S": "TE",
    "3SM": "LUI",
    "3SF": "LEI",
    "1P": "NOI",
    "2P": "VOI",
    "3P": "LORO",
    "3PM": "LORO",
    "3PF": "LORO",
}

numbers = [
    "DUE",
    "TRE",
    "QUATTRO",
    "CINQUE",
    "SEI",
    "SETTE",
    "OTTO",
    "NOVE",
    "DIECI",
    "ventitré".upper(),
]


class AbstractSemRole(metaclass=abc.ABCMeta):
    def __init__(self, f1, f2, f3, neg=False, calling_type=None):
        self.f1 = sanitize(f1)
        self.f2 = [sanitize(x) for x in f2]
        self.f3 = sanitize(f3)
        self.neg = neg

        self.f4 = ABSTRACT_SEM_ROLE

        self.pronoun = False

        f1: str = f1.upper()
        if f1 in _pron_pers:
            self.pronoun = f1
            self.f1 = _pron_pers[f1]
        elif any(x == split for x in numbers for split in f1.split()):
            # Ho visto quattro simpatici amici
            # = Ho visto 4 simpatici amici
            for i, n in enumerate(numbers, start=2):
                if n in f1:
                    self.f1 = f1.replace(n, str(i))
                    break
        elif f1 in _clitics_io and calling_type == DativeSemRole:
            print("sono qua 12312")
            self.pronoun = f1
            self.f1 = _clitics_io[f1]
        elif f1 in _clitics_do:
            self.pronoun = f1
            self.f1 = _clitics_do[f1]
        elif f1 in _feature_pronoun:
            self.pronoun = _feature_pronoun[f1]
        elif f1 == "":  # cov_sub not found
            self.f1 = "QUALCUNO\\QUALCOSA"

        self.code = self.get_code()

    def get_code(self):
        string = self.f2[0] + self.f3
        return hashlib.md5(string.encode()).hexdigest()

    def is_same_sign(self, other: "AbstractSemRole"):
        return self.neg == other.neg

    def is_positive(self) -> bool:
        return not self.neg

    def is_negative(self) -> bool:
        return self.neg

    def __lt__(self, other):
        return str(self) < str(other)

    def __eq__(self, other):
        res = (
            self.f1 == other.f1
            and self.f2[0] == other.f2[0]
            and self.f3 == other.f3
            and getattr(self, "neg", False) == getattr(other, "neg", False)
        ) or (
            self.f1 == other.f1
            and getattr(self, "neg", False) == getattr(other, "neg", False)
            and self.f2[0] == other.f2[0]
            and any(hasattr(x, "embedder") for x in [self, other])
        )
        return res

    def __hash__(self):
        return hash(str(self))

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"{self.f1}, {self.f2}, {self.f3}"


class AmbiguousSemRole:
    def __init__(self, f1, f2, role1: AbstractSemRole, role2: AbstractSemRole):
        self.f1 = sanitize(f1)
        self.f2 = [sanitize(x) for x in f2]
        self.roles = [role1, role2]
        for r in self.roles:
            r.embedded = True
        self.embedder = True
        self.f3 = "None"
        self.neg = False
        self.f4 = AMBIGUOUS_SEM_ROLE

    def as_qa(self) -> str:
        return " or ".join(x.as_qa() for x in self.roles)

    def is_same_sign(self, other: "AbstractSemRole"):
        return self.neg == other.neg

    def is_positive(self) -> bool:
        return not self.neg

    def is_negative(self) -> bool:
        return self.neg

    def __eq__(self, other):
        return any(x == other for x in self.roles)

    def __hash__(self):
        return sum(hash(x) for x in self.roles)

    def __str__(self) -> str:
        return " or ".join(str(x) for x in self.roles)


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

    def __init__(self, f1: str, f2: List[str], f3: str, neg=False, calling_type=None):
        assert f3 in ["ACTIVE", ACTV_S, "PASSIVE"], f3
        super().__init__(f1, f2, f3, neg, calling_type)
        if f2[0] in class_2_verbs_si:
            self.f3 = ACTV_S
        self.f4 = ORDINARY_SEM_ROLE

    def as_qa(self):
        v = self.f2[0]
        f1 = (self.pronoun if self.pronoun else self.f1).upper()
        if self.f3 == "ACTIVE":
            return f"Chi o cosa {third_person_formation(v)}? {f1}"
        elif self.f3 == ACTV_S:
            return f"Chi o cosa {third_person_formation(v, include_si=True)}? {f1}"
        elif self.f3 == "PASSIVE":
            return f"Chi o cosa è {past_part_formation(v)}? {f1}"

    def __str__(self):
        v = self.f2[0]
        f1 = (self.pronoun if self.pronoun else self.f1).upper()
        if self.f3 == "ACTIVE":
            return f"{f1} è chi o cosa {third_person_formation(v)}"
        elif self.f3 == ACTV_S:
            return f"{f1} è chi o cosa {third_person_formation(v, include_si=True)}"
        elif self.f3 == "PASSIVE":
            return f"{f1} è chi o cosa è {past_part_formation(v)}"


class SuppSemRole(OrdinarySemRole):
    def __init__(self, f1, f2, f3, worded=False, neg=False):
        super().__init__(f1, f2, f3, neg)
        self.f4 = SUPP_SEM_ROLE
        self.worded = worded

    def copy(self):
        return SuppSemRole(self.f1, self.f2, self.f3)

    def __str__(self):
        if self.worded:
            return super().__str__() + " " + ", ".join(x.lower() for x in self.f2[1:])
        return super().__str__()


class SuppSemRoleVADV(OrdinarySemRole):
    def __init__(self, f1, f2, f3, neg=False):
        super().__init__(f1, f2, f3, neg)
        self.f4 = SUPP_SEM_ROLE

    def __str__(self):
        return super().__str__() + " " + " ".join(map(lambda x: x.lower(), self.f2[1:]))


class MetterePrepSemRole(OrdinarySemRole):
    def __init__(self, f1, f2, f3, non_verbal_origin: List[Tag], neg=False):
        super().__init__(f1, f2, f3, neg)
        self.f4 = METTERE_PREP_SEM_ROLE
        self.non_verbal_origin = " ".join(x.occ for x in non_verbal_origin)


class AteSemRole(OrdinarySemRole):
    def __init__(self, f1, f2, f3, non_verbal_origin: List[str], neg=False):
        super().__init__(f1, f2, f3, neg)
        self.f4 = ATE_SEM_ROLE
        self.non_verbal_origin = " ".join(non_verbal_origin)


class CausativeSemRole(OrdinarySemRole):
    def __init__(self, f1, f2, f3, inf: str, neg=False):
        super().__init__(f1, f2, f3, neg)
        if inf in class_2_verbs_si:
            inf = reflexive_infinitive_formation(inf)
        self.inf = sanitize(inf)
        self.f4 = CAUSATIVE_SEM_ROLE

    def as_qa(self):
        f1 = (self.pronoun if self.pronoun else self.f1).upper()
        tmp = sanitize(get_determinative_inf(self.inf).occ + " " + self.inf)
        return f"Chi o cosa determina {tmp}? {f1}"

    def __eq__(self, other):
        return super().__eq__(other) and self.inf == other.inf

    __hash__ = AbstractSemRole.__hash__

    def __str__(self):
        f1 = (self.pronoun if self.pronoun else self.f1).upper()
        tmp = sanitize(get_determinative_inf(self.inf).occ + " " + self.inf)
        return f"{f1} è chi o cosa determina {tmp}"


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

    def __init__(self, f1: str, f3: str, neg=False):
        super().__init__(f1, ["svolgere", "professione", f3], "ACTIVE", neg)
        self.f4 = JOB_SEM_ROLE

    def as_qa(self):
        if len(self.f2) > 2:
            return f"Chi svolge la professione di {self.f2[2]}? {self.f1}"
        else:
            return f"Chi svolge una professione? {self.f1}"

    def copy(self) -> "JobSemRole":
        return JobSemRole(self.f1, self.f2[2])

    def __str__(self):
        f1 = (self.pronoun if self.pronoun else self.f1).upper()
        if len(self.f2) > 2:
            return f"{f1} è chi svolge la professione di {self.f2[2]}"
        else:
            return f"{f1} è chi svolge una professione"


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

    def __init__(self, f1, f2, neg=False):
        verb = f2[0]
        f3 = ACTV_S  # Luigi consegna un pacco a Piero => PIero è a chi si consegna
        if verb in two_place_predicate2:
            f3 = ACTV  # A Luigi piace il gelato => Luigi è a chi piace [qualcosa ...]
        super().__init__(f1, f2, f3, neg, calling_type=DativeSemRole)
        self.f4 = DATIVE_SEM_ROLE

    def as_qa(self):
        f1 = self.f1
        if self.f1 in _feature_pronoun:
            f1 = _feature_pronoun[self.f1]
        v = self.f2[0].lower()
        vc = third_person_formation(v, include_si=self.f3 == ACTV_S)

        tmp = f1.split()
        prefix = None
        if tmp[0] == "I":
            prefix = "A"
        elif tmp[0] in {"LA", "LO"}:
            prefix = "AL"
        elif tmp[0] in {"IL"}:
            prefix = "AL "
            del tmp[0]
        else:
            tmp = ["A"] + tmp
        if prefix:
            tmp[0] = prefix + tmp[0]

        f1 = " ".join(tmp)
        if v in trivalent_verbs:
            return f"A chi {vc} qualcosa? {f1}"
        else:
            return f"A chi {vc}? {f1}"

    def __str__(self):
        f1 = (self.pronoun if self.pronoun else self.f1).upper()
        v = self.f2[0].lower()
        vc = third_person_formation(v, include_si=self.f3 == ACTV_S)
        if v in trivalent_verbs | two_place_predicate2:
            return f"{f1} è a chi {vc} qualcosa"
        else:
            return f"{f1} è a chi o cosa {vc}"
