from typing import List

import pytest

from nlpytaly import NLPYTALY
from ..SemRole import (
    AbstractSemRole,
    OrdinarySemRole,
)
from ..utils import list_equals_no_order


@pytest.fixture()
def tagger():
    return NLPYTALY()


def test1(tagger):
    result = tagger.tag("Mario ha messo sotto accusa il suo amico")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("MARIO", ["accusare"], "ACTIVE",),
        OrdinarySemRole("IL SUO AMICO", ["accusare"], "PASSIVE",),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test2(tagger):
    result = tagger.tag("L'imputato fu messo sotto chiave dal poliziotto")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("IL POLIZIOTTO", ["rinchiudere"], "ACTIVE",),
        OrdinarySemRole("L' IMPUTATO", ["rinchiudere"], "PASSIVE",),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test3(tagger):
    result = tagger.tag("Il tenente ha messo sotto sorveglianza la scuola")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("IL TENENTE", ["sorvegliare"], "ACTIVE",),
        OrdinarySemRole("LA SCUOLA", ["sorvegliare"], "PASSIVE",),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test4(tagger):
    result = tagger.tag("La duchessa è stata messa all'indice dalla corte")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("LA CORTE", ["accusare"], "ACTIVE",),
        OrdinarySemRole("LA DUCHESSA", ["accusare"], "PASSIVE",),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test5(tagger):
    result = tagger.tag("Mia nuora è stata messa sotto sorveglianza dalla suocera")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("la suocera", ["sorvegliare"], "ACTIVE",),
        OrdinarySemRole("mia nuora", ["sorvegliare"], "PASSIVE",),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test6(tagger):
    result = tagger.tag("Sara ha messo sotto contratto Marco")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("sara", ["assumere"], "ACTIVE",),
        OrdinarySemRole("marco", ["assumere"], "PASSIVE",),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


# def test3(tagger):
#     result = tagger.tag("Si sono messi agli arresti gli studenti")
#     actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
#     expected_sem_roles = [
#         OrdinarySemRole("GLI STUDENTI", ["arrestare"], "PASSIVE",),
#     ]
#     list_equals_no_order(actual_sem_roles, expected_sem_roles)
