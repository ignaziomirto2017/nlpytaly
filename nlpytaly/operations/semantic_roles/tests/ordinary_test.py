from typing import List

import pytest

from nlpytaly import NLPYTALY
from ..utils import list_equals_no_order
from ....Tag import Tag
from ....operations.semantic_roles.PredFinder import OrdinarySemRole, DativeSemRole


@pytest.fixture()
def tagger():
    return NLPYTALY()


def test1(tagger):
    result = tagger.tag("La maestra bacchetta gli alunni.")
    actual_sem_roles: List[Tag] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("LA MAESTRA", ["bacchettare"], "ACTIVE"),
        OrdinarySemRole("GLI ALUNNI", ["bacchettare"], "PASSIVE"),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test2(tagger):
    result = tagger.tag("Gli alunni vennero bacchettati dalla maestra")
    actual_sem_roles: List[Tag] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("LA MAESTRA", ["bacchettare"], "ACTIVE"),
        OrdinarySemRole("GLI ALUNNI", ["bacchettare"], "PASSIVE"),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test3(tagger):
    result = tagger.tag("Luigi mangia la pasta")
    actual_sem_roles: List[Tag] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("LUIGI", ["mangiare"], "ACTIVE"),
        OrdinarySemRole("LA PASTA", ["mangiare"], "PASSIVE"),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test4(tagger):
    result = tagger.tag("Giovanni si lava")
    actual_sem_roles: List[Tag] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("GIOVANNI", ["lavare"], "ACTIVE"),
        OrdinarySemRole("GIOVANNI", ["lavare"], "PASSIVE"),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test5(tagger):
    result = tagger.tag("Ci vogliono dei soldi")
    actual_sem_roles: List[Tag] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("DEI SOLDI", ["servire"], "ACTIVE"),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test6(tagger):
    result = tagger.tag("Loro ci vogliono bene")
    actual_sem_roles: List[Tag] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("LORO", ["amare"], "ACTIVE"),
        OrdinarySemRole("CI", ["amare"], "PASSIVE"),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test7(tagger):
    result = tagger.tag("L'uomo aggredito ha denunciato gli assalitori")
    actual_sem_roles: List[Tag] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("L' UOMO AGGREDITO", ["denunciare"], "ACTIVE"),
        OrdinarySemRole("L' UOMO", ["aggredire"], "PASSIVE"),
        OrdinarySemRole("GLI ASSALITORI", ["denunciare"], "PASSIVE"),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test8(tagger):
    result = tagger.tag("Mario si consegna la merce")
    actual_sem_roles: List[Tag] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("MARIO", ["consegnare"], "ACTIVE"),
        DativeSemRole("MARIO", ["consegnare"]),
        OrdinarySemRole("LA MERCE", ["consegnare"], "PASSIVE"),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test9(tagger):
    result = tagger.tag("ha pubblicato suoi lavori")
    actual_sem_roles: List[Tag] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("LUI|LEI", ["pubblicare"], "ACTIVE"),
        OrdinarySemRole("SUOI LAVORI", ["pubblicare"], "PASSIVE"),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test10(tagger):
    result = tagger.tag("Il medico ha prescritto a Piero una terapia antibiotica")
    actual_sem_roles: List[Tag] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("IL MEDICO", ["prescrivere"], "ACTIVE"),
        OrdinarySemRole("UNA TERAPIA ANTIBIOTICA", ["prescrivere"], "PASSIVE"),
        DativeSemRole("PIERO", ["prescrivere"]),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


# def test11(tagger):
#     result = tagger.tag("Il sergente si è pentito")
#     actual_sem_roles: List[Tag] = result["sem_roles"]
#     expected_sem_roles = [
#         OrdinarySemRole("IL SERGENTE", ["pentire"], "ACTIVE_SI"),
#     ]
#     list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test12(tagger):
    result = tagger.tag(
        "Fava cominciò a raccogliere elementi per dimostrare i conflitti di interesse"
    )
    actual_sem_roles: List[Tag] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("FAVA", ["cominciare"], "ACTIVE"),
        OrdinarySemRole("QUALCUNO\\QUALCOSA", ["raccogliere"], "ACTIVE"),
        OrdinarySemRole("ELEMENTI", ["raccogliere"], "PASSIVE"),
        OrdinarySemRole("QUALCUNO\\QUALCOSA", ["dimostrare"], "ACTIVE"),
        OrdinarySemRole("I CONFLITTI", ["dimostrare"], "PASSIVE"),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test13(tagger):
    result = tagger.tag(
        "Berlino nel 1945 evitò il default perché il suo debito fu dimezzato dai Paesi"
    )
    actual_sem_roles: List[Tag] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("BERLINO", ["evitare"], "ACTIVE"),
        OrdinarySemRole("IL DEFAULT", ["evitare"], "PASSIVE"),
        OrdinarySemRole("I PAESI", ["dimezzare"], "ACTIVE"),
        OrdinarySemRole("IL SUO DEBITO", ["dimezzare"], "PASSIVE"),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test14(tagger):
    result = tagger.tag("La ragazza è andata ieri in biblioteca per ritirare dei libri")
    actual_sem_roles: List[Tag] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("la ragazza", ["andare"], "ACTIVE"),
        OrdinarySemRole("QUALCUNO\\QUALCOSA", ["ritirare"], "ACTIVE"),
        OrdinarySemRole("dei libri", ["ritirare"], "PASSIVE"),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test15(tagger):
    result = tagger.tag("La persona accusata è stata liberata")
    actual_sem_roles: List[Tag] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("la persona", ["accusare"], "PASSIVE"),
        OrdinarySemRole("la persona accusata", ["liberare"], "PASSIVE"),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test16(tagger):
    result = tagger.tag("Marco ha consegnato la merce all'amico")
    actual_sem_roles: List[Tag] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("marco", ["consegnare"], "ACTIVE"),
        OrdinarySemRole("la merce", ["consegnare"], "PASSIVE"),
        DativeSemRole("l' amico", ["consegnare"]),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test17(tagger):
    result = tagger.tag("L'epidemia spopola l'area")
    actual_sem_roles: List[Tag] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("l' epidemia", ["spopolare"], "ACTIVE"),
        OrdinarySemRole("l' area", ["spopolare"], "PASSIVE"),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test18(tagger):
    result = tagger.tag("Mia madre pettina Giovanna")
    actual_sem_roles: List[Tag] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("mia madre", ["pettinare"], "ACTIVE"),
        OrdinarySemRole("giovanna", ["pettinare"], "PASSIVE"),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


# def test19(tagger):
#     result = tagger.tag("Mario vuole bene a Sandra")
#     actual_sem_roles: List[Tag] = result["sem_roles"]
#     expected_sem_roles = [
#         OrdinarySemRole("mario", ["amare"], "ACTIVE"),
#         OrdinarySemRole("sandra", ["amare"], "PASSIVE"),
#     ]
#     list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test20(tagger):
    result = tagger.tag("Mi sono accanito e ho perduto")
    actual_sem_roles: List[Tag] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("io", ["accanire"], "ACTIVE_SI"),
        OrdinarySemRole("io", ["perdere"], "ACTIVE"),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test21(tagger):
    result = tagger.tag(
        "Il commissario ha messo sotto torchio il ragazzo arrestato ieri"
    )
    actual_sem_roles: List[Tag] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("il commissario", ["torchiare"], "ACTIVE"),
        OrdinarySemRole("il ragazzo arrestato", ["torchiare"], "PASSIVE"),
        OrdinarySemRole("il ragazzo", ["arrestare"], "PASSIVE"),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test22(tagger):
    result = tagger.tag(
        "La polizia arrivata ieri a Roma è intervenuta per disperdere dei giovani manifestanti"
    )
    actual_sem_roles: List[Tag] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("la polizia", ["arrivare"], "ACTIVE"),
        OrdinarySemRole("la polizia arrivata", ["intervenire"], "ACTIVE"),
        OrdinarySemRole("qualcuno\\qualcosa", ["disperdere"], "ACTIVE"),
        OrdinarySemRole("dei giovani manifestanti", ["disperdere"], "PASSIVE"),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test23(tagger):
    result = tagger.tag(
        "Le autorità hanno interrotto la manifestazione contro il razzismo perché questi giovani hanno rotto delle vetrate lanciando sampietrini"
    )
    actual_sem_roles: List[Tag] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("Le autorità", ["interrompere"], "ACTIVE"),
        OrdinarySemRole("la manifestazione", ["interrompere"], "PASSIVE"),
        OrdinarySemRole("questi giovani", ["rompere"], "ACTIVE"),
        OrdinarySemRole("delle vetrate", ["rompere"], "ACTIVE_SI"),
        OrdinarySemRole("qualcuno\\qualcosa", ["lanciare"], "ACTIVE"),
        OrdinarySemRole("sampietrini", ["lanciare"], "PASSIVE"),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test24(tagger):
    result = tagger.tag(
        "I manifestanti erano stati precedentemente avvisati dalla polizia usando dei megafoni"
    )
    actual_sem_roles: List[Tag] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("La polizia", ["avvisare"], "ACTIVE"),
        OrdinarySemRole("I manifestanti", ["avvisare"], "PASSIVE"),
        OrdinarySemRole("qualcuno\\qualcosa", ["usare"], "ACTIVE"),
        OrdinarySemRole("dei megafoni", ["usare"], "PASSIVE"),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test25(tagger):
    result = tagger.tag("Le immagini viste in TV hanno scioccato gli Italiani")
    actual_sem_roles: List[Tag] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("Le immagini viste", ["scioccare"], "ACTIVE"),
        OrdinarySemRole("Le immagini", ["vedere"], "PASSIVE"),
        OrdinarySemRole("gli Italiani", ["scioccare"], "PASSIVE"),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test26(tagger):
    result = tagger.tag(
        "I manifestanti hanno anche violato delle regole imposte dal Covid"
    )
    actual_sem_roles: List[Tag] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("I manifestanti", ["violare"], "ACTIVE"),
        OrdinarySemRole("delle regole imposte", ["violare"], "PASSIVE"),
        OrdinarySemRole("delle regole", ["imporre"], "PASSIVE"),
        OrdinarySemRole("il covid", ["imporre"], "ACTIVE"),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)
