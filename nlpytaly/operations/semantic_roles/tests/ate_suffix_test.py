from typing import List

import pytest

from nlpytaly import NLPYTALY

from ....data.ate_multiwords import (
    ate_multiwords,
    ate_multiwords_colpire,
    ate_multiwords_insultare,
)
from ..SemRole.consts import ACTV, PASSV
from ..SemRole.SemRole import AbstractSemRole, AteSemRole
from ..utils import list_equals_no_order


@pytest.fixture()
def tagger():
    return NLPYTALY()


def test1(tagger):
    result = tagger.tag("La maestra prende a bacchettate gli alunni.")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        AteSemRole("LA MAESTRA", ["bacchettare", "bacchettate"], ACTV, []),
        AteSemRole("GLI ALUNNI", ["bacchettare", "bacchettate"], PASSV, []),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test2(tagger):
    result = tagger.tag("Gli alunni furono presi a parolacce dalla maestra")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        AteSemRole("LA MAESTRA", ["insultare", "parolacce"], ACTV, []),
        AteSemRole("GLI ALUNNI", ["insultare", "parolacce"], PASSV, []),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


@pytest.mark.skip
def test3(tagger):
    result = tagger.tag("Si prendono i bambini a bacchettate")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        AteSemRole("I BAMBINI", ["bacchettare", "bacchettate"], PASSV, [])
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test4(tagger):
    result = tagger.tag("Gli alunni furono presi a parolacce da una maestra")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        AteSemRole("UNA MAESTRA", ["insultare", "parolacce"], ACTV, []),
        AteSemRole("GLI ALUNNI", ["insultare", "parolacce"], PASSV, []),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test5(tagger):
    result = tagger.tag("Gli alunni furono presi a parolacce da un'amica")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        AteSemRole("UN' AMICA", ["insultare", "parolacce"], ACTV, []),
        AteSemRole("GLI ALUNNI", ["insultare", "parolacce"], PASSV, []),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test6(tagger):
    result = tagger.tag(
        "L'amico è stato preso l'altro giorno a bacchettate dal preside"
    )
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        AteSemRole("L' AMICO", ["BACCHETTARE", "BACCHETTATE"], PASSV, []),
        AteSemRole("IL PRESIDE", ["BACCHETTARE", "BACCHETTATE"], ACTV, []),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test7(tagger):
    for n, v in ate_multiwords.items():
        for s in {f"Mario prende a {n} Luigi", f"Luigi è preso a {n} da Mario"}:
            result = tagger.tag(s)
            actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
            expected_sem_roles = [
                AteSemRole("MARIO", [v.upper(), n.upper()], ACTV, []),
                AteSemRole("LUIGI", [v.upper(), n.upper()], PASSV, []),
            ]
            list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test8(tagger):
    for n in ate_multiwords_colpire:
        for s in {f"Mario prende a {n} Luigi", f"Luigi è preso a {n} da Mario"}:
            result = tagger.tag(s)
            actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
            expected_sem_roles = [
                AteSemRole("MARIO", ["COLPIRE", n.upper()], ACTV, []),
                AteSemRole("LUIGI", ["COLPIRE", n.upper()], PASSV, []),
            ]
            list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test9(tagger):
    for n in ate_multiwords_insultare:
        for s in {f"Mario prende a {n} Luigi", f"Luigi è preso a {n} da Mario"}:
            result = tagger.tag(s)
            actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
            expected_sem_roles = [
                AteSemRole("MARIO", ["INSULTARE", n.upper()], ACTV, []),
                AteSemRole("LUIGI", ["INSULTARE", n.upper()], PASSV, []),
            ]
            list_equals_no_order(actual_sem_roles, expected_sem_roles)
