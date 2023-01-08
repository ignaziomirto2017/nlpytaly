from typing import List

import pytest

from nlpytaly import NLPYTALY
from nlpytaly.operations.semantic_roles.SemRole.consts import ACTV, ACTV_S, PASSV

from ..SemRole.SemRole import (
    AbstractSemRole,
    CausativeSemRole,
    DativeSemRole,
    OrdinarySemRole,
)
from ..utils import list_equals_no_order


@pytest.fixture()
def tagger():
    return NLPYTALY()


def test1(tagger):
    result = tagger.tag("Mario si è fatto visitare dal medico.")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("MARIO", ["visitare"], PASSV),
        OrdinarySemRole("IL MEDICO", ["visitare"], ACTV),
        CausativeSemRole("MARIO", ["fare"], ACTV, "visitare"),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test2(tagger):
    result = tagger.tag("Mario si è fatto comprare il pane da Luigi.")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        CausativeSemRole("MARIO", ["fare"], ACTV, "comprare"),
        OrdinarySemRole("LUIGI", ["comprare"], ACTV),
        OrdinarySemRole("IL PANE", ["comprare"], PASSV),
        DativeSemRole("MARIO", ["comprare"]),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test3(tagger):
    result = tagger.tag("Il professore si è fatto portare l'aranciata dal bambino.")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        CausativeSemRole("IL PROFESSORE", ["fare"], ACTV, "portare"),
        OrdinarySemRole("IL BAMBINO", ["portare"], ACTV),
        OrdinarySemRole("L' ARANCIATA", ["portare"], PASSV),
        DativeSemRole("IL PROFESSORE", ["portare"]),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test4(tagger):
    result = tagger.tag("Mario parla a Luigi.")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("MARIO", ["parlare"], ACTV),
        DativeSemRole("LUIGI", ["parlare"]),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test5(tagger):
    result = tagger.tag("Mario ha comprato il gelato al bambino.")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("MARIO", ["comprare"], ACTV),
        OrdinarySemRole("IL GELATO", ["comprare"], PASSV),
        DativeSemRole("IL BAMBINO", ["comprare"]),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test7(tagger):
    result = tagger.tag("Mario si fa aprire la porta dal suo amico.")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        CausativeSemRole("MARIO", ["fare"], ACTV, "aprire"),
        DativeSemRole("MARIO", ["aprire"]),
        OrdinarySemRole("IL SUO AMICO", ["aprire"], ACTV),
        OrdinarySemRole("LA PORTA", ["aprire"], PASSV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test8(tagger):
    result = tagger.tag("Luca fece giocare l'asso a Piero")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        CausativeSemRole("LUCA", ["fare"], ACTV, "giocare"),
        OrdinarySemRole("PIERO", ["giocare"], ACTV),
        OrdinarySemRole("L' ASSO", ["giocare"], PASSV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test9(tagger):
    result = tagger.tag("Maria ha dato la cartellina alla sorella")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("MARIA", ["dare"], ACTV),
        OrdinarySemRole("LA CARTELLINA", ["dare"], PASSV),
        DativeSemRole("LA SORELLA", ["dare"]),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test10(tagger):
    result = tagger.tag("Luigi sta pensando")
    tags = tagger.tags

    # testa il blocco
    assert [t.block for t in tags] == [1, 2, 2]

    # testa la diathesis
    for t in tags:
        if t.block == 2:
            assert t.is_active()
    assert tags[1].is_aux()
    assert tags[0].syntactic_role == "SOGG"

    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [OrdinarySemRole("LUIGI", ["pensare"], ACTV)]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test11(tagger):
    result = tagger.tag("Luigi sta mangiando le mele")
    tags = tagger.tags

    # testa il blocco
    assert [t.block for t in tags] == [1, 2, 2, 3, 3]

    # testa la diathesis
    for t in tags:
        if t.block == 2:
            assert t.is_active()
    assert tags[1].is_aux()
    assert tags[0].syntactic_role == "SOGG"
    assert tags[3].syntactic_role == "OD"
    assert tags[4].syntactic_role == "OD"

    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("LUIGI", ["mangiare"], ACTV),
        OrdinarySemRole("LE MELE", ["mangiare"], PASSV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test12(tagger):
    result = tagger.tag("Mangiando le mele, Mario è guarito")
    tags = tagger.tags

    # testa il blocco
    assert [t.block for t in tags] == [1, 2, 2, 3, 4, 5, 5]

    # testa la diathesis
    for t in tags:
        if t.block == 1:
            assert t.is_active()
    assert tags[1].syntactic_role == "OD"
    assert tags[2].syntactic_role == "OD"
    assert tags[4].syntactic_role == "SOGG"

    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("QUALCUNO\\QUALCOSA", ["mangiare"], ACTV),
        OrdinarySemRole("LE MELE", ["mangiare"], PASSV),
        OrdinarySemRole("MARIO", ["guarire"], PASSV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test13(tagger):
    result = tagger.tag("La collega si è fatta riportare i libri dalla studentessa")
    tags = tagger.tags

    # testa il blocco
    assert [t.block for t in tags] == [1, 1, 2, 2, 2, 2, 3, 3, 4, 4]

    # testa la diathesis
    for t in tags:
        if t.block == 2:
            assert t.is_middle_pr()
    assert tags[1].syntactic_role == "SOGG"
    assert tags[7].syntactic_role == "OD"

    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("I LIBRI", ["riportare"], PASSV),
        OrdinarySemRole("LA STUDENTESSA", ["riportare"], ACTV),
        CausativeSemRole("LA COLLEGA", ["fare"], ACTV, "riportare"),
        DativeSemRole("LA COLLEGA", ["riportare"]),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test15(tagger):
    result = tagger.tag("I professori si sono concessi una pausa")
    tags = tagger.tags

    # testa il blocco
    assert [t.block for t in tags] == [1, 1, 2, 2, 2, 3, 3]

    # testa la diathesis
    for t in tags:
        if t.block == 2:
            assert t.is_middle_pr()
    assert tags[0].syntactic_role == "SOGG"
    assert tags[1].syntactic_role == "SOGG"

    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("I PROFESSORI", ["concedere"], ACTV),
        DativeSemRole("I PROFESSORI", ["concedere"]),
        OrdinarySemRole("UNA PAUSA", ["concedere"], PASSV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test16(tagger):
    result = tagger.tag("I professori si sono lavati")
    tags = tagger.tags

    # testa il blocco
    assert [t.block for t in tags] == [1, 1, 2, 2, 2]

    # testa la diathesis
    for t in tags:
        if t.block == 2:
            assert t.is_middle_pr()
    assert tags[0].syntactic_role == "SOGG"
    assert tags[1].syntactic_role == "SOGG"

    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("I PROFESSORI", ["lavare"], ACTV),
        OrdinarySemRole("I PROFESSORI", ["lavare"], PASSV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test17(tagger):
    result = tagger.tag(
        "La polizia antisommossa arrivata ieri a Roma è intervenuta per disperdere dei manifestanti"
    )
    tags = tagger.tags

    # testa la diathesis
    for t in tags:
        if t.block == 3:
            assert t.is_middle_mr()
        if t.block == 4:
            assert t.is_active()

    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("LA POLIZIA ANTISOMMOSSA", ["ARRIVARE"], ACTV),
        OrdinarySemRole("LA POLIZIA ANTISOMMOSSA ARRIVATA", ["INTERVENIRE"], ACTV),
        OrdinarySemRole(r"QUALCUNO\QUALCOSA", ["DISPERDERE"], ACTV),
        OrdinarySemRole("DEI MANIFESTANTI", ["DISPERDERE"], PASSV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test18(tagger):
    result = tagger.tag(
        "Le autorità hanno interrotto la manifestazione contro il razzismo perché questi giovani hanno rotto delle vetrate lanciando dei sampietrini"
    )
    tags = tagger.tags

    # testa la diathesis
    for t in tags:
        if t.block in [2, 6, 8]:
            assert t.is_active()

    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("LE AUTORITÀ", ["INTERROMPERE"], ACTV),
        OrdinarySemRole("LA MANIFESTAZIONE", ["INTERROMPERE"], PASSV),
        OrdinarySemRole("QUESTI GIOVANI", ["ROMPERE"], ACTV),
        OrdinarySemRole("DELLE VETRATE", ["ROMPERE"], ACTV_S),
        OrdinarySemRole(r"QUALCUNO\QUALCOSA", ["LANCIARE"], ACTV),
        OrdinarySemRole("DEI SAMPIETRINI", ["LANCIARE"], PASSV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test19(tagger):
    result = tagger.tag(
        "I manifestanti erano stati precedentemente avvisati dalla polizia usando dei megafoni"
    )
    tags = tagger.tags

    # testa la diathesis
    for t in tags:
        if t.block == 2:
            assert t.is_passive()
        if t.block == 4:
            assert t.is_active()

    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("I MANIFESTANTI", ["AVVISARE", "precedentemente"], PASSV),
        OrdinarySemRole("LA POLIZIA", ["AVVISARE", "precedentemente"], ACTV),
        OrdinarySemRole(r"QUALCUNO\QUALCOSA", ["USARE"], ACTV),
        OrdinarySemRole("DEI MEGAFONI", ["USARE"], PASSV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test20(tagger):
    result = tagger.tag(
        "I disordini causati da questi manifestanti hanno fatto pronunciare al Primo Ministro le seguenti parole:"
    )
    tags = tagger.tags

    # testa la diathesis
    for t in tags:
        if t.block == 3:
            assert t.is_active()

    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("I DISORDINI", ["CAUSARE"], PASSV),
        OrdinarySemRole("QUESTI MANIFESTANTI", ["CAUSARE"], ACTV),
        CausativeSemRole("I DISORDINI CAUSATI", ["fare"], ACTV, "pronunciare"),
        OrdinarySemRole("IL PRIMO MINISTRO", ["PRONUNCIARE"], ACTV),
        OrdinarySemRole("LE SEGUENTI PAROLE", ["PRONUNCIARE"], PASSV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test21(tagger):
    result = tagger.tag("Le immagini viste in TV hanno scioccato gli italiani")
    tags = tagger.tags

    # testa la diathesis
    for t in tags:
        if t.block == 3:
            assert t.is_active()

    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("LE IMMAGINI", ["VEDERE"], PASSV),
        OrdinarySemRole("LE IMMAGINI VISTE", ["SCIOCCARE"], ACTV),
        OrdinarySemRole("GLI ITALIANI", ["SCIOCCARE"], PASSV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test22(tagger):
    result = tagger.tag(
        "I manifestanti hanno anche violato le regole imposte dal Covid"
    )
    tags = tagger.tags

    # testa la diathesis
    for t in tags:
        if t.block == 2:
            assert t.is_active()

    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("I MANIFESTANTI", ["VIOLARE"], ACTV),
        OrdinarySemRole("LE REGOLE IMPOSTE", ["VIOLARE"], PASSV),
        OrdinarySemRole("LE REGOLE", ["IMPORRE"], PASSV),
        OrdinarySemRole("IL COVID", ["IMPORRE"], ACTV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test23(tagger):
    result = tagger.tag("Il razzismo procura solo un gran danno all'Italia")
    tags = tagger.tags

    # testa la diathesis
    for t in tags:
        if t.block == 2:
            assert t.is_active()

    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("IL RAZZISMO", ["DANNEGGIARE"], ACTV),
        OrdinarySemRole("L' ITALIA", ["DANNEGGIARE"], PASSV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test24(tagger):
    result = tagger.tag("La maestra sta spesso elogiando i ragazzi")
    tags = tagger.tags

    # testa la diathesis
    for t in tags:
        if t.block == 2:
            assert t.is_active()

    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("LA MAESTRA", ["ELOGIARE"], ACTV),
        OrdinarySemRole("I RAGAZZI", ["ELOGIARE"], PASSV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)
