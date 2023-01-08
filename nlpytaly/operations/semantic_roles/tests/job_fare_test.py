from typing import List

import pytest

from nlpytaly import NLPYTALY

from ..SemRole.SemRole import AbstractSemRole, JobSemRole
from ..utils import list_equals_no_order


@pytest.fixture()
def tagger():
    return NLPYTALY()


def test1(tagger):
    result = tagger.tag("Mario ha fatto spesso il meccanico")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [JobSemRole("MARIO", "meccanico")]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)
