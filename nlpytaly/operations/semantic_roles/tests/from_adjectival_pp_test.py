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
    result = tagger.tag("I ragazzi arrivati ieri sono andati via")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("I RAGAZZI ARRIVATI", ["andare"], "ACTIVE",),
        OrdinarySemRole("I RAGAZZI", ["arrivare"], "ACTIVE",),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test2(tagger):
    result = tagger.tag("La moto aggiustata ieri oggi è stata lavata")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("LA MOTO AGGIUSTATA", ["lavare"], "PASSIVE",),
        OrdinarySemRole("LA MOTO", ["aggiustare"], "PASSIVE",),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test3(tagger):  # virgole dopo 'presidente' e prima di 'ha' fanno fallire il test
    result = tagger.tag(
        "Il presidente sollecitato nuovamente dai berlusconiani ha chiarito la questione"
    )
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("IL PRESIDENTE", ["sollecitare"], "PASSIVE",),
        OrdinarySemRole("I BERLUSCONIANI", ["sollecitare"], "ACTIVE",),
        OrdinarySemRole("IL PRESIDENTE SOLLECITATO", ["chiarire"], "ACTIVE",),
        OrdinarySemRole("LA QUESTIONE", ["chiarire"], "PASSIVE",),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)
