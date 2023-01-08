from typing import List

import pytest

from nlpytaly import NLPYTALY

from ....Test_utils import entail_each_other
from ..SemRole.consts import ACTV, PASSV
from ..SemRole.SemRole import AbstractSemRole, OrdinarySemRole
from ..utils import list_equals_no_order


@pytest.fixture()
def tagger():
    return NLPYTALY()


def test1(tagger):
    result = tagger.tag("Mario ha messo sotto accusa il suo amico")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("MARIO", ["accusare"], ACTV),
        OrdinarySemRole("IL SUO AMICO", ["accusare"], PASSV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test2(tagger):
    result = tagger.tag("L'imputato fu messo sotto chiave dal poliziotto")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("IL POLIZIOTTO", ["rinchiudere"], ACTV),
        OrdinarySemRole("L' IMPUTATO", ["rinchiudere"], PASSV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test3(tagger):
    result = tagger.tag("Il tenente ha messo sotto sorveglianza la scuola")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("IL TENENTE", ["sorvegliare"], ACTV),
        OrdinarySemRole("LA SCUOLA", ["sorvegliare"], PASSV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test4(tagger):
    result = tagger.tag("La duchessa è stata messa all'indice dalla corte")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("LA CORTE", ["accusare"], ACTV),
        OrdinarySemRole("LA DUCHESSA", ["accusare"], PASSV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test5(tagger):
    result = tagger.tag("Mia nuora è stata messa sotto sorveglianza dalla suocera")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("la suocera", ["sorvegliare"], ACTV),
        OrdinarySemRole("mia nuora", ["sorvegliare"], PASSV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test6(tagger):
    result = tagger.tag("Sara ha messo sotto contratto Marco")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("sara", ["assumere"], ACTV),
        OrdinarySemRole("marco", ["assumere"], PASSV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test7(tagger):
    result = tagger.tag("Le provette sono state messe sotto osservazione ")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [OrdinarySemRole("Le provette", ["controllare"], PASSV)]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test8(tagger):
    result = tagger.tag("Ha messo sotto sorveglianza la scuola")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("LUI|LEI", ["sorvegliare"], ACTV),
        OrdinarySemRole("LA SCUOLA", ["sorvegliare"], PASSV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test9(tagger):
    result = tagger.tag("Ha messo la scuola sotto sorveglianza")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("LUI|LEI", ["sorvegliare"], ACTV),
        OrdinarySemRole("LA SCUOLA", ["sorvegliare"], PASSV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test10_sotto(tagger):
    from ....data.mettere_prep import mettere_prep_dict
    from ....data.verbs.class_1_verbs import class_1_verbs
    from ....data.verbs.class_2_verbs import class_2_verbs
    from ...formations.past_part_formation import past_part_formation

    for prep in {"sotto", "in", "nel", "sul", "a", "al", "da", "di", "fuori"}:
        dict_ = mettere_prep_dict[prep]
        for sostantivo, v in dict_.items():
            if "v" not in v:
                continue
            verb = v["v"]
            if verb in class_1_verbs.union(class_2_verbs):
                continue
            s = f"Max ha messo l'amico {prep} {sostantivo}"
            t = f"L'amico è stato {past_part_formation(v['v'])} da Max"
            print(s, t)
            entail_each_other({s, t})
