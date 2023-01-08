from typing import List

import pytest

from nlpytaly import NLPYTALY

from ....Tag import Tag
from ..SemRole.consts import ACTV, ACTV_S, PASSV
from ..SemRole.SemRole import (
    AbstractSemRole,
    AteSemRole,
    CausativeSemRole,
    DativeSemRole,
    JobSemRole,
    MetterePrepSemRole,
    OrdinarySemRole,
)
from ..utils import list_equals_no_order


@pytest.fixture()
def tagger():
    return NLPYTALY()


def test1(tagger):
    result = tagger.tag("La donna fece intervenire i mariti.")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        CausativeSemRole("LA DONNA", ["fare"], ACTV, "intervenire"),
        OrdinarySemRole("I MARITI", ["intervenire"], ACTV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test2(tagger):
    result = tagger.tag("Mario ha fatto arrabbiare Luigi.")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        CausativeSemRole("MARIO", ["fare"], ACTV, "ARRABBIARSI"),
        OrdinarySemRole("LUIGI", ["ARRABBIARE"], ACTV_S),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test3(tagger):
    result = tagger.tag("Mario ha fatto pentire Luigi.")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        CausativeSemRole("MARIO", ["fare"], ACTV, "PENTIRSI"),
        OrdinarySemRole("LUIGI", ["PENTIRE"], ACTV_S),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test4(tagger):
    result = tagger.tag("Mario ha fatto prendere a legnate l'amico.")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        CausativeSemRole("MARIO", ["fare"], ACTV, "COLPIRE"),
        AteSemRole("L' AMICO", ["COLPIRE", "LEGNATE"], PASSV, ["LEGNATE"]),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test5(tagger):
    result = tagger.tag("Giorgio ha fatto prendere a parolacce l'amico dal preside.")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        CausativeSemRole("GIORGIO", ["fare"], ACTV, "INSULTARE"),
        AteSemRole("L' AMICO", ["INSULTARE", "PAROLACCE"], PASSV, ["PAROLACCE"]),
        AteSemRole("IL PRESIDE", ["INSULTARE", "PAROLACCE"], ACTV, ["PAROLACCE"]),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test6(tagger):
    result = tagger.tag("Giorgio ha fatto prendere a parolacce l'amico dal preside.")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        CausativeSemRole("GIORGIO", ["fare"], ACTV, "INSULTARE"),
        AteSemRole("L' AMICO", ["INSULTARE", "PAROLACCE"], PASSV, ["PAROLACCE"]),
        AteSemRole("IL PRESIDE", ["INSULTARE", "PAROLACCE"], ACTV, ["PAROLACCE"]),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test7(tagger):
    result = tagger.tag("Sandro fece mettere sotto accusa il suo amico dal preside")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        CausativeSemRole("SANDRO", ["fare"], ACTV, "ACCUSARE"),
        MetterePrepSemRole("IL SUO AMICO", ["ACCUSARE"], PASSV, []),
        MetterePrepSemRole("IL PRESIDE", ["ACCUSARE"], ACTV, []),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test8(tagger):
    result = tagger.tag("Leonardo è stato fatto prendere a parolacce dalla prof")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("LEONARDO", ["insultare", "parolacce"], PASSV),
        OrdinarySemRole("LA PROF", ["insultare", "parolacce"], ACTV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test9(tagger):
    result = tagger.tag("Il tecnico si è fatto ingannare dallo studente")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("LO STUDENTE", ["ingannare"], ACTV),
        OrdinarySemRole("IL TECNICO", ["ingannare"], PASSV),
        CausativeSemRole("IL TECNICO", ["fare"], ACTV, "INGANNARE"),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test10(tagger):
    result = tagger.tag("La donna fece intervenire le guardie")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        CausativeSemRole("LA DONNA", ["fare"], ACTV, "INTERVENIRE"),
        OrdinarySemRole("LE GUARDIE", ["intervenire"], ACTV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test11(tagger):
    result = tagger.tag("Piero fece dare le mele a Gianni da Sandro.")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        CausativeSemRole("PIERO", ["fare"], ACTV, "DARE"),
        OrdinarySemRole("LE MELE", ["dare"], PASSV),
        OrdinarySemRole("SANDRO", ["dare"], ACTV),
        DativeSemRole("GIANNI", ["dare"]),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test12(tagger):
    result = tagger.tag("Piero fece dare le mele da Sandro a Gianni.")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        CausativeSemRole("PIERO", ["fare"], ACTV, "DARE"),
        OrdinarySemRole("LE MELE", ["dare"], PASSV),
        OrdinarySemRole("SANDRO", ["dare"], ACTV),
        DativeSemRole("GIANNI", ["dare"]),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test13(tagger):
    result = tagger.tag("Roberto è stato fatto cadere da Luigi")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        CausativeSemRole("LUIGI", ["fare"], ACTV, "CADERE"),
        OrdinarySemRole("ROBERTO", ["cadere"], ACTV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test14(tagger):
    result = tagger.tag("La mamma ha fatto accompagnare il bambino dalla nonna")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        CausativeSemRole("LA MAMMA", ["fare"], ACTV, "ACCOMPAGNARE"),
        OrdinarySemRole("LA NONNA", ["accompagnare"], ACTV),
        OrdinarySemRole("IL BAMBINO", ["accompagnare"], PASSV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test15(tagger):
    result = tagger.tag("Lo sparo ha fatto imbizzarrire il cavallo")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        CausativeSemRole("LO SPARO", ["fare"], ACTV, "IMBIZZARRIRE"),
        OrdinarySemRole("IL CAVALLO", ["IMBIZZARRIRE"], ACTV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


# meronymy
def test16(tagger):
    result = tagger.tag("Sandra si è fatta pettinare i capelli dalla sorella")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        CausativeSemRole("SANDRA", ["fare"], ACTV, "pettinare"),
        DativeSemRole("SANDRA", ["pettinare"]),
        OrdinarySemRole("LA SORELLA", ["pettinare"], ACTV),
        OrdinarySemRole("I CAPELLI", ["pettinare"], PASSV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test17(tagger):
    result = tagger.tag("Mario si è fatto ingannare da Sandro")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        CausativeSemRole("MARIO", ["fare"], ACTV, "ingannare"),
        OrdinarySemRole("MARIO", ["ingannare"], PASSV),
        OrdinarySemRole("SANDRO", ["ingannare"], ACTV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test18(tagger):
    result = tagger.tag("Aldo fece mangiare patate a noi")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        CausativeSemRole("ALDO", ["fare"], ACTV, "mangiare"),
        OrdinarySemRole("PATATE", ["mangiare"], PASSV),
        OrdinarySemRole("NOI", ["mangiare"], ACTV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test19(tagger):
    result = tagger.tag("L'operazione ha fatto a lungo lamentare il paziente ")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        CausativeSemRole("L' operazione", ["fare"], ACTV, "lamentare"),
        OrdinarySemRole("IL PAZIENTE", ["lamentare"], ACTV_S),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test20(tagger):
    result = tagger.tag("Io mi sono fatto comprare il gelato dai bambini")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        CausativeSemRole("IO", ["fare"], ACTV, "comprare"),
        DativeSemRole("IO", ["comprare"]),
        OrdinarySemRole("I BAMBINI", ["comprare"], ACTV),
        OrdinarySemRole("IL GELATO", ["comprare"], PASSV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test21(tagger):
    result = tagger.tag(
        "Le donne addestrate da Sandra hanno fatto scoprire dei mondi nuovi agli amici"
    )
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("le donne", ["addestrare"], PASSV),
        OrdinarySemRole("Sandra", ["addestrare"], ACTV),
        CausativeSemRole("le donne addestrate", ["fare"], ACTV, "scoprire"),
        OrdinarySemRole("gli amici", ["scoprire"], ACTV),
        OrdinarySemRole("dei mondi nuovi", ["scoprire"], PASSV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test22(tagger):
    result = tagger.tag("Io mi sono fatto prescrivere una terapia antibiotica da Piero")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        CausativeSemRole("io", ["fare"], ACTV, "prescrivere"),
        DativeSemRole("IO", ["prescrivere"]),
        OrdinarySemRole("una terapia antibiotica", ["prescrivere"], PASSV),
        OrdinarySemRole("Piero", ["prescrivere"], ACTV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test23(tagger):
    result = tagger.tag(
        "Farà conoscere tramite i suoi canali social altri tre muri dove ha pubblicato suoi lavori"
    )
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        CausativeSemRole("lui|lei", ["fare"], ACTV, "conoscere"),
        OrdinarySemRole("altri tre muri", ["conoscere"], PASSV),
        OrdinarySemRole("lui|lei", ["pubblicare"], ACTV),
        OrdinarySemRole("suoi lavori", ["pubblicare"], PASSV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test24(tagger):
    result = tagger.tag("L'aria malsana ha fatto ammalare il ragazzo")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        CausativeSemRole("l' aria malsana", ["fare"], ACTV, "ammalare"),
        OrdinarySemRole("il ragazzo", ["ammalare"], ACTV_S),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test25(tagger):
    result = tagger.tag("Il prof si è fatto ingannare dall'alunno")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        CausativeSemRole("Il prof", ["fare"], ACTV, "ingannare"),
        OrdinarySemRole("Il prof", ["ingannare"], PASSV),
        OrdinarySemRole("l' alunno", ["ingannare"], ACTV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test26(tagger):
    result = tagger.tag(
        "Il magistrato ha fatto mettere sotto sorveglianza gli indagati "
    )
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        CausativeSemRole("Il magistrato", ["fare"], ACTV, "sorvegliare"),
        OrdinarySemRole("gli indagati", ["sorvegliare"], PASSV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test27(tagger):
    result = tagger.tag("Ha fatto mangiare patate a Sandro")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        CausativeSemRole("lui|lei", ["fare"], ACTV, "mangiare"),
        OrdinarySemRole("patate", ["mangiare"], PASSV),
        OrdinarySemRole("Sandro", ["mangiare"], ACTV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test28(tagger):
    result = tagger.tag("Sandra farà dare il premio alla sorella da Piero")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        CausativeSemRole("Sandra", ["fare"], ACTV, "dare"),
        OrdinarySemRole("il premio", ["dare"], PASSV),
        OrdinarySemRole("Piero", ["dare"], ACTV),
        DativeSemRole("la sorella", ["dare"]),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test29(tagger):
    result = tagger.tag(
        "I disordini causati da questi manifestanti hanno fatto pronunciare al Ministro le seguenti parole"
    )
    actual_sem_roles: List[Tag] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("I disordini", ["causare"], PASSV),
        OrdinarySemRole("questi manifestanti", ["causare"], ACTV),
        CausativeSemRole("I disordini causati", ["fare"], ACTV, "pronunciare"),
        OrdinarySemRole("il ministro", ["pronunciare"], ACTV),
        OrdinarySemRole("le seguenti parole", ["pronunciare"], PASSV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test30(tagger):
    result = tagger.tag("Le tue parole fanno vacillare le mie certezze")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        CausativeSemRole("Le tue parole", ["fare"], ACTV, "vacillare"),
        OrdinarySemRole("le mie certezze", ["vacillare"], ACTV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test31(tagger):
    result = tagger.tag("Gli studenti si sono fatti rincretinire dal professore")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        CausativeSemRole("Gli studenti", ["fare"], ACTV, "rincretinire"),
        OrdinarySemRole("Gli studenti", ["rincretinire"], PASSV),
        OrdinarySemRole("il professore", ["rincretinire"], ACTV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test32(tagger):
    result = tagger.tag("Io mi sono fatto aiutare dagli amici")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        CausativeSemRole("Io", ["fare"], ACTV, "aiutare"),
        OrdinarySemRole("Io", ["aiutare"], PASSV),
        OrdinarySemRole("gli amici", ["aiutare"], ACTV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test33(tagger):
    result = tagger.tag(
        "Lui si era fatto consegnare un assegno da un'imprenditrice per sbloccare le indagini sui danneggiamenti subiti dall’azienda agricola"
    )
    actual_sem_roles: List[Tag] = result["sem_roles"]
    expected_sem_roles = [
        CausativeSemRole("Lui", ["fare"], ACTV, "consegnare"),
        DativeSemRole("lui", ["consegnare"]),
        OrdinarySemRole("un'imprenditrice", ["consegnare"], ACTV),
        OrdinarySemRole("un assegno", ["consegnare"], PASSV),
        OrdinarySemRole("QUALCUNO\\QUALCOSA", ["sbloccare"], ACTV),
        OrdinarySemRole("le indagini", ["sbloccare"], PASSV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test34(tagger):
    result = tagger.tag("Mi sono fatto aiutare dagli amici")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        CausativeSemRole("Io", ["fare"], ACTV, "aiutare"),
        OrdinarySemRole("Io", ["aiutare"], PASSV),
        OrdinarySemRole("gli amici", ["aiutare"], ACTV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test35(tagger):
    result = tagger.tag("Mario ha fatto fare il meccanico a Gianni")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        CausativeSemRole("Mario", ["fare"], ACTV, "lavorare"),
        JobSemRole("Gianni", "meccanico"),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)
