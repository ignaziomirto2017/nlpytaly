from typing import List

import pytest

from nlpytaly import NLPYTALY
from nlpytaly.operations.semantic_roles.SemRole.consts import ACTV, ACTV_S, PASSV

from ....Tag import Tag
from ..SemRole.SemRole import (
    AbstractSemRole,
    DativeSemRole,
    OrdinarySemRole,
    SuppSemRole,
)
from ..utils import list_equals_no_order


@pytest.fixture()
def tagger():
    return NLPYTALY()


def test1(tagger):
    result = tagger.tag("Io ho fatto un'analisi")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [SuppSemRole("IO", ["analizzare"], ACTV)]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test2(tagger):
    result = tagger.tag("L'amico faceva molti errori.")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [SuppSemRole("L' AMICO", ["sbagliare"], ACTV)]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test3(tagger):
    result = tagger.tag("Sandro fa la corte a Maria")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        SuppSemRole("SANDRO", ["CORTEGGIARE"], ACTV),
        SuppSemRole("MARIA", ["CORTEGGIARE"], PASSV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test4(tagger):
    result = tagger.tag("L'artista ha profuso dell'impegno")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [SuppSemRole("L' ARTISTA", ["IMPEGNARE"], ACTV_S)]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test5(tagger):
    result = tagger.tag("Sara fece un sorriso ai suoi fratelli")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        SuppSemRole("SARA", ["sorridere"], ACTV),
        DativeSemRole("I SUOI FRATELLI", ["sorridere"]),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test6(tagger):
    result = tagger.tag(
        "L'ospite consultato dalla Rai ha dato dei consigli agli esperti"
    )
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("l' ospite", ["consultare"], PASSV),
        OrdinarySemRole("la Rai", ["consultare"], ACTV),
        SuppSemRole("l' ospite consultato", ["consigliare"], ACTV),
        DativeSemRole("gli esperti", ["consigliare"]),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test7(tagger):
    result = tagger.tag("Mario ha dato una stiratina ai panni")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        SuppSemRole("Mario", ["STIRARE"], ACTV),
        SuppSemRole("i panni", ["STIRARE"], PASSV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test8(tagger):
    result = tagger.tag("Mario ha fatto una stiratina")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [SuppSemRole("Mario", ["STIRARE"], ACTV)]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test9(tagger):
    result = tagger.tag("Il razzismo procura solo un gran danno all'Italia")
    actual_sem_roles: List[Tag] = result["sem_roles"]
    expected_sem_roles = [
        SuppSemRole("Il razzismo", ["danneggiare"], ACTV),
        SuppSemRole("l'Italia", ["danneggiare"], PASSV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test10(tagger):
    result = tagger.tag("Mario ha paura")
    actual_sem_roles: List[Tag] = result["sem_roles"]
    expected_sem_roles = [SuppSemRole("Mario", ["impaurire"], PASSV)]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test11(tagger):
    result = tagger.tag("Mario sta facendo una doccia")
    actual_sem_roles: List[Tag] = result["sem_roles"]
    expected_sem_roles = [SuppSemRole("Mario", ["lavare"], ACTV_S)]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test12(tagger):
    result = tagger.tag("Piero ha fatto un dono allo zio")
    actual_sem_roles: List[Tag] = result["sem_roles"]
    expected_sem_roles = [
        SuppSemRole("Piero", ["donare"], ACTV),
        DativeSemRole("lo zio", ["donare"]),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test13(tagger):
    result = tagger.tag("Gli amici hanno mosso un appunto ai cugini")
    actual_sem_roles: List[Tag] = result["sem_roles"]
    expected_sem_roles = [
        SuppSemRole("gli amici", ["biasimare"], ACTV),
        SuppSemRole("i cugini", ["biasimare"], PASSV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test14(tagger):
    result = tagger.tag("Mario ha dato una scorsa al libro")
    actual_sem_roles: List[Tag] = result["sem_roles"]
    expected_sem_roles = [
        SuppSemRole("Mario", ["guardare"], ACTV),
        SuppSemRole("il libro", ["guardare"], PASSV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test15(tagger):
    result = tagger.tag("I detenuti evasi hanno commesso una rapina")
    actual_sem_roles: List[Tag] = result["sem_roles"]
    expected_sem_roles = [SuppSemRole("I detenuti evasi", ["rapinare"], ACTV)]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test16(tagger):
    result = tagger.tag("Mario ha fatto un grande sforzo")
    actual_sem_roles: List[Tag] = result["sem_roles"]
    expected_sem_roles = [SuppSemRole("Mario", ["sforzare"], ACTV_S)]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test17(tagger):
    result = tagger.tag("Mario ha solo fatto uno sfogo")
    actual_sem_roles: List[Tag] = result["sem_roles"]
    expected_sem_roles = [SuppSemRole("Mario", ["sfogare"], ACTV_S)]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test18(tagger):
    result = tagger.tag("Mario ha solo fatto una provocazione al collega")
    actual_sem_roles: List[Tag] = result["sem_roles"]
    expected_sem_roles = [
        SuppSemRole("Mario", ["provocare"], ACTV),
        SuppSemRole("il collega", ["provocare"], PASSV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test19(tagger):  # manca il ruolo con di-phrase
    result = tagger.tag("Mario ha fatto sfoggio di cravatte")
    actual_sem_roles: List[Tag] = result["sem_roles"]
    expected_sem_roles = [SuppSemRole("Mario", ["sfoggiare"], ACTV)]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test20(tagger):
    result = tagger.tag("Mario ha fatto delle angherie a Fabio")
    actual_sem_roles: List[Tag] = result["sem_roles"]
    expected_sem_roles = [
        SuppSemRole("Mario", ["vessare"], ACTV),
        SuppSemRole("Fabio", ["vessare"], PASSV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test21(tagger):
    result = tagger.tag("Lei scoccò a Luca un sorriso ammaliatore")
    actual_sem_roles: List[Tag] = result["sem_roles"]
    expected_sem_roles = [
        SuppSemRole("Lei", ["SORRIDERE"], ACTV),
        DativeSemRole("Luca", ["SORRIDERE"]),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test22(tagger):
    result = tagger.tag("Max ha dato delle delucidazioni al collega")
    actual_sem_roles: List[Tag] = result["sem_roles"]
    expected_sem_roles = [
        SuppSemRole("Max", ["Spiegare"], ACTV),
        DativeSemRole("il collega", ["Spiegare"]),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test23(tagger):
    result = tagger.tag("Mario ha fatto una scempiaggine")
    actual_sem_roles: List[Tag] = result["sem_roles"]
    expected_sem_roles = [SuppSemRole("Mario", ["comportare"], ACTV_S)]

    # per controllare il secondo elemento di f2
    assert actual_sem_roles[0].f2 == ["COMPORTARE", "STUPIDAMENTE"]

    list_equals_no_order(actual_sem_roles, expected_sem_roles)
