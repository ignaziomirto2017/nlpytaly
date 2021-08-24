from typing import List

import pytest

from nlpytaly import NLPYTALY
from ..SemRole import SuppSemRole, AbstractSemRole, DativeSemRole, OrdinarySemRole
from ..utils import list_equals_no_order
from ....Tag import Tag


@pytest.fixture()
def tagger():
    return NLPYTALY()


def test1(tagger):
    result = tagger.tag("Io ho fatto un'analisi")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        SuppSemRole("IO", ["analizzare"], "ACTIVE",),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test2(tagger):
    result = tagger.tag("L'amico faceva molti errori.")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        SuppSemRole("L' AMICO", ["sbagliare"], "ACTIVE",),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test3(tagger):
    result = tagger.tag("Sandro fa la corte a Maria")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        SuppSemRole("SANDRO", ["CORTEGGIARE"], "ACTIVE",),
        SuppSemRole("MARIA", ["CORTEGGIARE"], "PASSIVE",),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test4(tagger):
    result = tagger.tag("L'artista ha profuso dell'impegno")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        SuppSemRole("L' ARTISTA", ["IMPEGNARE"], "ACTIVE_SI",),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test5(tagger):
    result = tagger.tag("Sara fece un sorriso ai suoi fratelli")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        SuppSemRole("SARA", ["sorridere"], "ACTIVE",),
        DativeSemRole("I SUOI FRATELLI", ["sorridere"]),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test6(tagger):
    result = tagger.tag(
        "L'ospite consultato dalla Rai ha dato dei consigli agli esperti"
    )
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("l' ospite", ["consultare"], "PASSIVE",),
        OrdinarySemRole("la Rai", ["consultare"], "ACTIVE",),
        SuppSemRole("l' ospite consultato", ["consigliare"], "ACTIVE",),
        SuppSemRole("gli esperti", ["consigliare"], "PASSIVE",),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test7(tagger):
    result = tagger.tag("Mario ha dato una stiratina ai panni")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        SuppSemRole("Mario", ["STIRARE"], "ACTIVE",),
        SuppSemRole("i panni", ["STIRARE"], "PASSIVE",),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test8(tagger):
    result = tagger.tag("Mario ha fatto una stiratina")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        SuppSemRole("Mario", ["STIRARE"], "ACTIVE",),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test9(tagger):
    result = tagger.tag("Il razzismo procura solo un gran danno all'Italia")
    actual_sem_roles: List[Tag] = result["sem_roles"]
    expected_sem_roles = [
        SuppSemRole("Il razzismo", ["danneggiare"], "ACTIVE"),
        SuppSemRole("l'Italia", ["danneggiare"], "PASSIVE"),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)
