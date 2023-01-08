from typing import List

import pytest

from nlpytaly import NLPYTALY
from nlpytaly.operations.semantic_roles.SemRole.consts import ACTV, PASSV

from ....operations.semantic_roles.SemRole.SemRole import DativeSemRole, OrdinarySemRole
from ....Tag import Tag
from ..utils import list_equals_no_order


@pytest.fixture()
def tagger():
    return NLPYTALY()


def test1(tagger):
    result = tagger.tag("Mario le vede")
    actual_sem_roles: List[Tag] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("MARIO", ["vedere"], ACTV),
        OrdinarySemRole("3PF", ["vedere"], PASSV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test2(tagger):
    result = tagger.tag("Mario le ha dato la posta")
    actual_sem_roles: List[Tag] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("MARIO", ["dare"], ACTV),
        OrdinarySemRole("LA POSTA", ["dare"], PASSV),
        DativeSemRole("3SF", ["dare"]),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test3(tagger):
    result = tagger.tag("Mario le parla")
    actual_sem_roles: List[Tag] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("MARIO", ["parlare"], ACTV),
        DativeSemRole("3SF", ["parlare"]),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)
