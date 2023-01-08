from typing import List

import pytest

from nlpytaly import NLPYTALY

from ..SemRole.consts import ACTV, PASSV
from ..SemRole.SemRole import AbstractSemRole, OrdinarySemRole
from ..utils import list_equals_no_order


@pytest.fixture()
def tagger():
    return NLPYTALY()


def test1(tagger):
    result = tagger.tag("I ragazzi arrivati ieri sono andati via")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("I RAGAZZI ARRIVATI", ["andare"], ACTV),
        OrdinarySemRole("I RAGAZZI", ["arrivare"], ACTV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test2(tagger):
    result = tagger.tag("La moto aggiustata ieri oggi è stata lavata")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("LA MOTO AGGIUSTATA", ["lavare"], PASSV),
        OrdinarySemRole("LA MOTO", ["aggiustare"], PASSV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test3(tagger):  # virgole dopo 'presidente' e prima di 'ha' fanno fallire il test
    result = tagger.tag(
        "Il presidente sollecitato nuovamente dai berlusconiani ha chiarito la questione"
    )
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("IL PRESIDENTE", ["sollecitare"], PASSV),
        OrdinarySemRole("I BERLUSCONIANI", ["sollecitare"], ACTV),
        OrdinarySemRole("IL PRESIDENTE SOLLECITATO", ["chiarire"], ACTV),
        OrdinarySemRole("LA QUESTIONE", ["chiarire"], PASSV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)
