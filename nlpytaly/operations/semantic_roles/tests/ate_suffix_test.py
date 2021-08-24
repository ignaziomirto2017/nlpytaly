from typing import List

import pytest

from nlpytaly import NLPYTALY
from ..SemRole import AteSemRole, AbstractSemRole
from ..utils import list_equals_no_order


@pytest.fixture()
def tagger():
    return NLPYTALY()


def test1(tagger):
    result = tagger.tag("La maestra prende a bacchettate gli alunni.")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        AteSemRole("LA MAESTRA", ["bacchettare", "bacchettate"], "ACTIVE", []),
        AteSemRole("GLI ALUNNI", ["bacchettare", "bacchettate"], "PASSIVE", []),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test2(tagger):
    result = tagger.tag("Gli alunni furono presi a parolacce dalla maestra")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        AteSemRole("LA MAESTRA", ["insultare", "parolacce"], "ACTIVE", []),
        AteSemRole("GLI ALUNNI", ["insultare", "parolacce"], "PASSIVE", []),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test3(tagger):
    result = tagger.tag("Si prendono i bambini a bacchettate")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        AteSemRole("I BAMBINI", ["bacchettare", "bacchettate"], "PASSIVE", []),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test4(tagger):
    result = tagger.tag("Gli alunni furono presi a parolacce da una maestra")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        AteSemRole("UNA MAESTRA", ["insultare", "parolacce"], "ACTIVE", []),
        AteSemRole("GLI ALUNNI", ["insultare", "parolacce"], "PASSIVE", []),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test5(tagger):
    result = tagger.tag("Gli alunni furono presi a parolacce da un'amica")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        AteSemRole("UN' AMICA", ["insultare", "parolacce"], "ACTIVE", []),
        AteSemRole("GLI ALUNNI", ["insultare", "parolacce"], "PASSIVE", []),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test6(tagger):
    result = tagger.tag(
        "L'amico è stato preso l'altro giorno a bacchettate dal preside"
    )
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        AteSemRole("L' AMICO", ["BACCHETTARE", "BACCHETTATE"], "PASSIVE", []),
        AteSemRole("IL PRESIDE", ["BACCHETTARE", "BACCHETTATE"], "ACTIVE", []),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)
