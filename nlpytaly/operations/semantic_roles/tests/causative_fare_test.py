from typing import List

import pytest

from nlpytaly import NLPYTALY
from ..SemRole import (
    AteSemRole,
    CausativeSemRole,
    OrdinarySemRole,
    MetterePrepSemRole,
    DativeSemRole,
    AbstractSemRole,
)
from ..utils import list_equals_no_order


@pytest.fixture()
def tagger():
    return NLPYTALY()


def test1(tagger):
    result = tagger.tag("La donna fece intervenire i mariti.")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        CausativeSemRole("LA DONNA", ["fare"], "ACTIVE", "intervenire"),
        OrdinarySemRole("I MARITI", ["intervenire"], "ACTIVE"),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test2(tagger):
    result = tagger.tag("Mario ha fatto arrabbiare Luigi.")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        CausativeSemRole("MARIO", ["fare"], "ACTIVE", "ARRABBIARSI"),
        OrdinarySemRole("LUIGI", ["ARRABBIARE"], "ACTIVE_SI"),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test3(tagger):
    result = tagger.tag("Mario ha fatto pentire Luigi.")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        CausativeSemRole("MARIO", ["fare"], "ACTIVE", "PENTIRSI"),
        OrdinarySemRole("LUIGI", ["PENTIRE"], "ACTIVE_SI"),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test4(tagger):
    result = tagger.tag("Mario ha fatto prendere a legnate l'amico.")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        CausativeSemRole("MARIO", ["fare"], "ACTIVE", "COLPIRE"),
        AteSemRole("L' AMICO", ["COLPIRE", "LEGNATE"], "PASSIVE", ["LEGNATE"]),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test5(tagger):
    result = tagger.tag("Giorgio ha fatto prendere a parolacce l'amico dal preside.")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        CausativeSemRole("GIORGIO", ["fare"], "ACTIVE", "INSULTARE"),
        AteSemRole("L' AMICO", ["INSULTARE", "PAROLACCE"], "PASSIVE", ["PAROLACCE"]),
        AteSemRole("IL PRESIDE", ["INSULTARE", "PAROLACCE"], "ACTIVE", ["PAROLACCE"]),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test6(tagger):
    result = tagger.tag("Giorgio ha fatto prendere a parolacce l'amico dal preside.")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        CausativeSemRole("GIORGIO", ["fare"], "ACTIVE", "INSULTARE"),
        AteSemRole("L' AMICO", ["INSULTARE", "PAROLACCE"], "PASSIVE", ["PAROLACCE"]),
        AteSemRole("IL PRESIDE", ["INSULTARE", "PAROLACCE"], "ACTIVE", ["PAROLACCE"]),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test7(tagger):
    result = tagger.tag("Sandro fece mettere sotto accusa il suo amico dal preside")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        CausativeSemRole("SANDRO", ["fare"], "ACTIVE", "ACCUSARE"),
        MetterePrepSemRole("IL SUO AMICO", ["ACCUSARE"], "PASSIVE", []),
        MetterePrepSemRole("IL PRESIDE", ["ACCUSARE"], "ACTIVE", []),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test8(tagger):
    result = tagger.tag("Leonardo è stato fatto prendere a parolacce dalla prof")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("LEONARDO", ["insultare", "parolacce"], "PASSIVE"),
        OrdinarySemRole("LA PROF", ["insultare", "parolacce"], "ACTIVE"),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test9(tagger):
    result = tagger.tag("Il tecnico si è fatto ingannare dallo studente")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("LO STUDENTE", ["ingannare"], "ACTIVE"),
        OrdinarySemRole("IL TECNICO", ["ingannare"], "PASSIVE"),
        CausativeSemRole("IL TECNICO", ["fare"], "ACTIVE", "INGANNARE"),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test10(tagger):
    result = tagger.tag("La donna fece intervenire le guardie")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        CausativeSemRole("LA DONNA", ["fare"], "ACTIVE", "INTERVENIRE"),
        OrdinarySemRole("LE GUARDIE", ["intervenire",], "ACTIVE",),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test11(tagger):
    result = tagger.tag("Piero fece dare le mele a Gianni da Sandro.")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        CausativeSemRole("PIERO", ["fare"], "ACTIVE", "DARE"),
        OrdinarySemRole("LE MELE", ["dare",], "PASSIVE",),
        OrdinarySemRole("SANDRO", ["dare",], "ACTIVE",),
        DativeSemRole("GIANNI", ["dare"]),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test12(tagger):
    result = tagger.tag("Piero fece dare le mele da Sandro a Gianni.")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        CausativeSemRole("PIERO", ["fare"], "ACTIVE", "DARE"),
        OrdinarySemRole("LE MELE", ["dare",], "PASSIVE",),
        OrdinarySemRole("SANDRO", ["dare",], "ACTIVE",),
        DativeSemRole("GIANNI", ["dare"]),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test13(tagger):
    result = tagger.tag("Roberto è stato fatto cadere da Luigi")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        CausativeSemRole("LUIGI", ["fare"], "ACTIVE", "CADERE"),
        OrdinarySemRole("ROBERTO", ["cadere"], "ACTIVE"),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test14(tagger):
    result = tagger.tag("La mamma ha fatto accompagnare il bambino dalla nonna")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        CausativeSemRole("LA MAMMA", ["fare"], "ACTIVE", "ACCOMPAGNARE"),
        OrdinarySemRole("LA NONNA", ["accompagnare"], "ACTIVE"),
        OrdinarySemRole("IL BAMBINO", ["accompagnare"], "PASSIVE"),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test15(tagger):
    result = tagger.tag("Lo sparo ha fatto imbizzarrire il cavallo")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        CausativeSemRole("LO SPARO", ["fare"], "ACTIVE", "IMBIZZARRIRE"),
        OrdinarySemRole("IL CAVALLO", ["IMBIZZARRIRE"], "ACTIVE"),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


# meronymy
def test16(tagger):
    result = tagger.tag("Sandra si è fatta pettinare i capelli dalla sorella")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        CausativeSemRole("SANDRA", ["fare"], "ACTIVE", "pettinare"),
        DativeSemRole("SANDRA", ["pettinare"]),
        OrdinarySemRole("LA SORELLA", ["pettinare"], "ACTIVE"),
        OrdinarySemRole("I CAPELLI", ["pettinare"], "PASSIVE"),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test17(tagger):
    result = tagger.tag("Mario si è fatto ingannare da Sandro")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        CausativeSemRole("MARIO", ["fare"], "ACTIVE", "ingannare"),
        OrdinarySemRole("MARIO", ["ingannare"], "PASSIVE"),
        OrdinarySemRole("SANDRO", ["ingannare"], "ACTIVE"),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test18(tagger):
    result = tagger.tag("Aldo fece mangiare patate a noi")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        CausativeSemRole("ALDO", ["fare"], "ACTIVE", "mangiare"),
        OrdinarySemRole("PATATE", ["mangiare"], "PASSIVE"),
        OrdinarySemRole("NOI", ["mangiare"], "ACTIVE"),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test19(tagger):
    result = tagger.tag("L'operazione ha fatto a lungo lamentare il paziente ")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        CausativeSemRole("L' operazione", ["fare"], "ACTIVE", "lamentare"),
        OrdinarySemRole("IL PAZIENTE", ["lamentare"], "ACTIVE_SI"),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test20(tagger):
    result = tagger.tag("Io mi sono fatto comprare il gelato dai bambini")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        CausativeSemRole("IO", ["fare"], "ACTIVE", "comprare"),
        DativeSemRole("IO", ["comprare"]),
        OrdinarySemRole("I BAMBINI", ["comprare"], "ACTIVE"),
        OrdinarySemRole("IL GELATO", ["comprare"], "PASSIVE"),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test21(tagger):
    result = tagger.tag(
        "Le donne addestrate da Sandra hanno fatto scoprire dei mondi nuovi agli amici"
    )
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("le donne", ["addestrare"], "PASSIVE"),
        OrdinarySemRole("Sandra", ["addestrare"], "ACTIVE"),
        CausativeSemRole("le donne addestrate", ["fare"], "ACTIVE", "scoprire"),
        OrdinarySemRole("gli amici", ["scoprire"], "ACTIVE"),
        OrdinarySemRole("dei mondi nuovi", ["scoprire"], "PASSIVE"),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test22(tagger):
    result = tagger.tag("Io mi sono fatto prescrivere una terapia antibiotica da Piero")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        CausativeSemRole("io", ["fare"], "ACTIVE", "prescrivere"),
        DativeSemRole("IO", ["prescrivere"]),
        OrdinarySemRole("una terapia antibiotica", ["prescrivere"], "PASSIVE"),
        OrdinarySemRole("Piero", ["prescrivere"], "ACTIVE"),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test23(tagger):
    result = tagger.tag(
        "Farà conoscere tramite i suoi canali social altri tre muri dove ha pubblicato suoi lavori"
    )
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        CausativeSemRole("lui|lei", ["fare"], "ACTIVE", "conoscere"),
        OrdinarySemRole("altri tre muri", ["conoscere"], "PASSIVE"),
        OrdinarySemRole("lui|lei", ["pubblicare"], "ACTIVE"),
        OrdinarySemRole("suoi lavori", ["pubblicare"], "PASSIVE"),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test24(tagger):
    result = tagger.tag("L'aria malsana ha fatto ammalare il ragazzo")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        CausativeSemRole("l' aria malsana", ["fare"], "ACTIVE", "ammalare"),
        OrdinarySemRole("il ragazzo", ["ammalare"], "ACTIVE_SI"),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test25(tagger):
    result = tagger.tag("Il prof si è fatto ingannare dall'alunno")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        CausativeSemRole("Il prof", ["fare"], "ACTIVE", "ingannare"),
        OrdinarySemRole("Il prof", ["ingannare"], "PASSIVE"),
        OrdinarySemRole("l' alunno", ["ingannare"], "ACTIVE"),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test26(tagger):
    result = tagger.tag(
        "Il magistrato ha fatto mettere sotto sorveglianza gli indagati "
    )
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        CausativeSemRole("Il magistrato", ["fare"], "ACTIVE", "sorvegliare"),
        OrdinarySemRole("gli indagati", ["sorvegliare"], "PASSIVE"),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test27(tagger):
    result = tagger.tag("Ha fatto mangiare patate a Sandro")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        CausativeSemRole("lui|lei", ["fare"], "ACTIVE", "mangiare"),
        OrdinarySemRole("patate", ["mangiare"], "PASSIVE"),
        OrdinarySemRole("Sandro", ["mangiare"], "ACTIVE"),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test28(tagger):
    result = tagger.tag("Sandra farà dare il premio alla sorella da Piero")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        CausativeSemRole("Sandra", ["fare"], "ACTIVE", "dare"),
        OrdinarySemRole("il premio", ["dare"], "PASSIVE"),
        OrdinarySemRole("Piero", ["dare"], "ACTIVE"),
        DativeSemRole("la sorella", ["dare"]),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test29(tagger):
    result = tagger.tag(
        "I disordini causati da questi manifestanti hanno fatto pronunciare al Ministro le seguenti parole"
    )
    actual_sem_roles: List[Tag] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("I disordini", ["causare"], "PASSIVE"),
        OrdinarySemRole("questi manifestanti", ["causare"], "ACTIVE"),
        CausativeSemRole("I disordini causati", ["fare"], "ACTIVE", "pronunciare"),
        OrdinarySemRole("il ministro", ["pronunciare"], "ACTIVE"),
        OrdinarySemRole("le seguenti parole", ["pronunciare"], "PASSIVE"),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test30(tagger):
    result = tagger.tag("Le tue parole fanno vacillare le mie certezze")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        CausativeSemRole("Le tue parole", ["fare"], "ACTIVE", "vacillare"),
        OrdinarySemRole("le mie certezze", ["vacillare"], "ACTIVE"),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test31(tagger):
    result = tagger.tag("Gli studenti si sono fatti rincretinire dal professore")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        CausativeSemRole("Gli studenti", ["fare"], "ACTIVE", "rincretinire"),
        OrdinarySemRole("Gli studenti", ["rincretinire"], "PASSIVE"),
        OrdinarySemRole("il professore", ["rincretinire"], "ACTIVE"),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test32(tagger):  # Senza overt subject fare causativo non riconosciuto
    result = tagger.tag("Io mi sono fatto aiutare dagli amici")
    actual_sem_roles: List[AbstractSemRole] = result["sem_roles"]
    expected_sem_roles = [
        CausativeSemRole("Io", ["fare"], "ACTIVE", "aiutare"),
        OrdinarySemRole("Io", ["aiutare"], "PASSIVE"),
        OrdinarySemRole("gli amici", ["aiutare"], "ACTIVE"),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)
