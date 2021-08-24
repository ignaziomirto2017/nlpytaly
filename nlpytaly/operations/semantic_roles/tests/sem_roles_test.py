from typing import List

import pytest

from nlpytaly import NLPYTALY
from ..SemRole import (
    AbstractSemRole,
    OrdinarySemRole,
    CausativeSemRole,
    DativeSemRole,
)
from ..utils import list_equals_no_order


@pytest.fixture()
def tagger():
    return NLPYTALY()


def test1(tagger):
    result = tagger.tag("Mario si è fatto visitare dal medico.")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("MARIO", ["visitare"], "PASSIVE"),
        OrdinarySemRole("IL MEDICO", ["visitare"], "ACTIVE"),
        CausativeSemRole("MARIO", ["fare"], "ACTIVE", "visitare"),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test2(tagger):
    result = tagger.tag("Mario si è fatto comprare il pane da Luigi.")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        CausativeSemRole("MARIO", ["fare"], "ACTIVE", "comprare"),
        OrdinarySemRole("LUIGI", ["comprare"], "ACTIVE"),
        OrdinarySemRole("IL PANE", ["comprare"], "PASSIVE"),
        DativeSemRole("MARIO", ["comprare"]),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test3(tagger):
    result = tagger.tag("Il professore si è fatto portare l'aranciata dal bambino.")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        CausativeSemRole("IL PROFESSORE", ["fare"], "ACTIVE", "portare"),
        OrdinarySemRole("IL BAMBINO", ["portare"], "ACTIVE"),
        OrdinarySemRole("L' ARANCIATA", ["portare"], "PASSIVE"),
        DativeSemRole("IL PROFESSORE", ["portare"]),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test4(tagger):
    result = tagger.tag("Mario parla a Luigi.")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("MARIO", ["parlare"], "ACTIVE"),
        DativeSemRole("LUIGI", ["parlare"]),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test5(tagger):
    result = tagger.tag("Mario ha comprato il gelato al bambino.")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("MARIO", ["comprare"], "ACTIVE"),
        OrdinarySemRole("IL GELATO", ["comprare"], "PASSIVE"),
        DativeSemRole("IL BAMBINO", ["comprare"]),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


# def test6(tagger):
#     result = tagger.tag("Mario si è fatto arrivare un pacco.")
#     actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
#     expected_sem_roles = [
#         CausativeSemRole("MARIO", ["fare"], "ACTIVE", "arrivare"),
#         # TODO
#         # OrdinarySemRole("IL PACCO", ["arrivare"], "ACTIVE"),
#     ]
#     list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test7(tagger):
    result = tagger.tag("Mario si fa aprire la porta dal suo amico.")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        CausativeSemRole("MARIO", ["fare"], "ACTIVE", "aprire"),
        DativeSemRole("MARIO", ["aprire"]),
        OrdinarySemRole("IL SUO AMICO", ["aprire"], "ACTIVE"),
        OrdinarySemRole("LA PORTA", ["aprire"], "PASSIVE"),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test8(tagger):
    result = tagger.tag("Luca fece giocare l'asso a Piero")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        CausativeSemRole("LUCA", ["fare"], "ACTIVE", "giocare"),
        OrdinarySemRole("PIERO", ["giocare"], "ACTIVE"),
        OrdinarySemRole("L' ASSO", ["giocare"], "PASSIVE"),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test9(tagger):
    result = tagger.tag("Maria ha dato la cartellina alla sorella")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("MARIA", ["dare"], "ACTIVE"),
        OrdinarySemRole("LA CARTELLINA", ["dare"], "PASSIVE"),
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
    expected_sem_roles = [
        OrdinarySemRole("LUIGI", ["pensare"], "ACTIVE"),
    ]
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
        OrdinarySemRole("LUIGI", ["mangiare"], "ACTIVE"),
        OrdinarySemRole("LE MELE", ["mangiare"], "PASSIVE"),
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
        OrdinarySemRole("QUALCUNO\\QUALCOSA", ["mangiare"], "ACTIVE"),
        OrdinarySemRole("LE MELE", ["mangiare"], "PASSIVE"),
        OrdinarySemRole("MARIO", ["guarire"], "PASSIVE"),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test13(tagger):
    result = tagger.tag("La collega si è fatta riportare i libri dalla studentessa")
    tags = tagger.tags

    # testa il blocco
    assert [t.block for t in tags] == [
        1,
        1,
        2,
        2,
        2,
        2,
        3,
        3,
        4,
        4,
    ]

    # testa la diathesis
    for t in tags:
        if t.block == 2:
            assert t.is_middle_pr()
    assert tags[1].syntactic_role == "SOGG"
    assert tags[7].syntactic_role == "OD"

    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("I LIBRI", ["riportare"], "PASSIVE"),
        OrdinarySemRole("LA STUDENTESSA", ["riportare"], "ACTIVE"),
        CausativeSemRole("LA COLLEGA", ["fare"], "ACTIVE", "riportare"),
        DativeSemRole("LA COLLEGA", ["riportare"]),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


# def test14(tagger):
#     result = tagger.tag("Loro vogliono bene solo a noi")
#     tags = tagger.tags

#     # testa il blocco
#     assert [t.block for t in tags] == [1, 2, 2, 2, 3, 3]

#     # testa la diathesis
#     for t in tags:
#         if t.block == 2:
#             assert t.is_active()
#     assert tags[0].ruolo_sintattico == "SOGG"

#     actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
#     expected_sem_roles = [
#         OrdinarySemRole("LORO", ["amare"], "ACTIVE"),
#         OrdinarySemRole("NOI", ["amare"], "PASSIVE"),
#     ]
#     list_equals_no_order(actual_sem_roles, expected_sem_roles)


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
        OrdinarySemRole("I PROFESSORI", ["concedere"], "ACTIVE"),
        DativeSemRole("I PROFESSORI", ["concedere"]),
        OrdinarySemRole("UNA PAUSA", ["concedere"], "PASSIVE"),
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
        OrdinarySemRole("I PROFESSORI", ["lavare"], "ACTIVE"),
        OrdinarySemRole("I PROFESSORI", ["lavare"], "PASSIVE"),
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
        OrdinarySemRole("LA POLIZIA ANTISOMMOSSA", ["ARRIVARE"], "ACTIVE"),
        OrdinarySemRole("LA POLIZIA ANTISOMMOSSA ARRIVATA", ["INTERVENIRE"], "ACTIVE"),
        OrdinarySemRole(r"QUALCUNO\QUALCOSA", ["DISPERDERE"], "ACTIVE"),
        OrdinarySemRole("DEI MANIFESTANTI", ["DISPERDERE"], "PASSIVE"),
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
        OrdinarySemRole("LE AUTORITÀ", ["INTERROMPERE"], "ACTIVE"),
        OrdinarySemRole("LA MANIFESTAZIONE", ["INTERROMPERE"], "PASSIVE"),
        OrdinarySemRole("QUESTI GIOVANI", ["ROMPERE"], "ACTIVE"),
        OrdinarySemRole("DELLE VETRATE", ["ROMPERE"], "ACTIVE_SI"),
        OrdinarySemRole(r"QUALCUNO\QUALCOSA", ["LANCIARE"], "ACTIVE"),
        OrdinarySemRole("DEI SAMPIETRINI", ["LANCIARE"], "PASSIVE"),
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
        OrdinarySemRole("I MANIFESTANTI", ["AVVISARE"], "PASSIVE"),
        OrdinarySemRole("LA POLIZIA", ["AVVISARE"], "ACTIVE"),
        OrdinarySemRole(r"QUALCUNO\QUALCOSA", ["USARE"], "ACTIVE"),
        OrdinarySemRole("DEI MEGAFONI", ["USARE"], "PASSIVE"),
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
        OrdinarySemRole("I DISORDINI", ["CAUSARE"], "PASSIVE"),
        OrdinarySemRole("QUESTI MANIFESTANTI", ["CAUSARE"], "ACTIVE"),
        CausativeSemRole("I DISORDINI CAUSATI", ["fare"], "ACTIVE", "pronunciare"),
        OrdinarySemRole("IL PRIMO MINISTRO", ["PRONUNCIARE"], "ACTIVE"),
        OrdinarySemRole("LE SEGUENTI PAROLE", ["PRONUNCIARE"], "PASSIVE"),
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
        OrdinarySemRole("LE IMMAGINI", ["VEDERE"], "PASSIVE"),
        OrdinarySemRole("LE IMMAGINI VISTE", ["SCIOCCARE"], "ACTIVE"),
        OrdinarySemRole("GLI ITALIANI", ["SCIOCCARE"], "PASSIVE"),
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
        OrdinarySemRole("I MANIFESTANTI", ["VIOLARE"], "ACTIVE"),
        OrdinarySemRole("LE REGOLE IMPOSTE", ["VIOLARE"], "PASSIVE"),
        OrdinarySemRole("LE REGOLE", ["IMPORRE"], "PASSIVE"),
        OrdinarySemRole("IL COVID", ["IMPORRE"], "ACTIVE"),
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
        OrdinarySemRole("IL RAZZISMO", ["DANNEGGIARE"], "ACTIVE"),
        OrdinarySemRole("L' ITALIA", ["DANNEGGIARE"], "PASSIVE"),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)
