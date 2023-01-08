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
    result = tagger.tag("La maestra bacchetta gli alunni.")
    actual_sem_roles: List[Tag] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("LA MAESTRA", ["bacchettare"], ACTV),
        OrdinarySemRole("GLI ALUNNI", ["bacchettare"], PASSV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test2(tagger):
    result = tagger.tag("Gli alunni vennero bacchettati dalla maestra")
    actual_sem_roles: List[Tag] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("LA MAESTRA", ["bacchettare"], ACTV),
        OrdinarySemRole("GLI ALUNNI", ["bacchettare"], PASSV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test3(tagger):
    result = tagger.tag("Luigi mangia la pasta")
    actual_sem_roles: List[Tag] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("LUIGI", ["mangiare"], ACTV),
        OrdinarySemRole("LA PASTA", ["mangiare"], PASSV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test4(tagger):
    result = tagger.tag("Giovanni si lava")
    actual_sem_roles: List[Tag] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("GIOVANNI", ["lavare"], ACTV),
        OrdinarySemRole("GIOVANNI", ["lavare"], PASSV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test5(tagger):
    result = tagger.tag("Ci vogliono dei soldi")
    actual_sem_roles: List[Tag] = result["sem_roles"]
    expected_sem_roles = [OrdinarySemRole("DEI SOLDI", ["servire"], ACTV)]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test6(tagger):
    result = tagger.tag("Loro ci vogliono bene")
    actual_sem_roles: List[Tag] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("LORO", ["amare"], ACTV),
        OrdinarySemRole("CI", ["amare"], PASSV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test7(tagger):
    result = tagger.tag("L'uomo aggredito ha denunciato gli assalitori")
    actual_sem_roles: List[Tag] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("L' UOMO AGGREDITO", ["denunciare"], ACTV),
        OrdinarySemRole("L' UOMO", ["aggredire"], PASSV),
        OrdinarySemRole("GLI ASSALITORI", ["denunciare"], PASSV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test8(tagger):
    result = tagger.tag("Mario si consegna la merce")
    actual_sem_roles: List[Tag] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("MARIO", ["consegnare"], ACTV),
        DativeSemRole("MARIO", ["consegnare"]),
        OrdinarySemRole("LA MERCE", ["consegnare"], PASSV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test9(tagger):
    result = tagger.tag("ha pubblicato suoi lavori")
    actual_sem_roles: List[Tag] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("LUI|LEI", ["pubblicare"], ACTV),
        OrdinarySemRole("SUOI LAVORI", ["pubblicare"], PASSV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test10(tagger):
    result = tagger.tag("Il medico ha prescritto a Piero una terapia antibiotica")
    actual_sem_roles: List[Tag] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("IL MEDICO", ["prescrivere"], ACTV),
        OrdinarySemRole("UNA TERAPIA ANTIBIOTICA", ["prescrivere"], PASSV),
        DativeSemRole("PIERO", ["prescrivere"]),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test12(tagger):
    result = tagger.tag(
        "Fava cominciò a raccogliere elementi per dimostrare i conflitti di interesse"
    )
    actual_sem_roles: List[Tag] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("FAVA", ["cominciare"], ACTV),
        OrdinarySemRole("QUALCUNO\\QUALCOSA", ["raccogliere"], ACTV),
        OrdinarySemRole("ELEMENTI", ["raccogliere"], PASSV),
        OrdinarySemRole("QUALCUNO\\QUALCOSA", ["dimostrare"], ACTV),
        OrdinarySemRole("I CONFLITTI", ["dimostrare"], PASSV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test13(tagger):
    result = tagger.tag(
        "Berlino nel 1945 evitò il default perché il suo debito fu dimezzato dai Paesi"
    )
    actual_sem_roles: List[Tag] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("BERLINO", ["evitare"], ACTV),
        OrdinarySemRole("IL DEFAULT", ["evitare"], PASSV),
        OrdinarySemRole("I PAESI", ["dimezzare"], ACTV),
        OrdinarySemRole("IL SUO DEBITO", ["dimezzare"], PASSV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test14(tagger):
    result = tagger.tag("La ragazza è andata ieri in biblioteca per ritirare dei libri")
    actual_sem_roles: List[Tag] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("la ragazza", ["andare"], ACTV),
        OrdinarySemRole("QUALCUNO\\QUALCOSA", ["ritirare"], ACTV),
        OrdinarySemRole("dei libri", ["ritirare"], PASSV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test15(tagger):
    result = tagger.tag("La persona accusata è stata liberata")
    actual_sem_roles: List[Tag] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("la persona", ["accusare"], PASSV),
        OrdinarySemRole("la persona accusata", ["liberare"], PASSV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test16(tagger):
    result = tagger.tag("Marco ha consegnato la merce all'amico")
    actual_sem_roles: List[Tag] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("marco", ["consegnare"], ACTV),
        OrdinarySemRole("la merce", ["consegnare"], PASSV),
        DativeSemRole("l' amico", ["consegnare"]),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test17(tagger):
    result = tagger.tag("L'epidemia spopola l'area")
    actual_sem_roles: List[Tag] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("l' epidemia", ["spopolare"], ACTV),
        OrdinarySemRole("l' area", ["spopolare"], PASSV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test18(tagger):
    result = tagger.tag("Mia madre pettina Giovanna")
    actual_sem_roles: List[Tag] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("mia madre", ["pettinare"], ACTV),
        OrdinarySemRole("giovanna", ["pettinare"], PASSV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test20(tagger):
    result = tagger.tag("Mi sono accanito e ho perduto")
    actual_sem_roles: List[Tag] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("io", ["accanire"], "ACTIVE_SI"),
        OrdinarySemRole("io", ["perdere"], ACTV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test21(tagger):
    result = tagger.tag(
        "Il commissario ha messo sotto torchio il ragazzo arrestato ieri"
    )
    actual_sem_roles: List[Tag] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("il commissario", ["torchiare"], ACTV),
        OrdinarySemRole("il ragazzo arrestato", ["torchiare"], PASSV),
        OrdinarySemRole("il ragazzo", ["arrestare"], PASSV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test22(tagger):
    result = tagger.tag(
        "La polizia arrivata ieri a Roma è intervenuta per disperdere dei giovani manifestanti"
    )
    actual_sem_roles: List[Tag] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("la polizia", ["arrivare"], ACTV),
        OrdinarySemRole("la polizia arrivata", ["intervenire"], ACTV),
        OrdinarySemRole("qualcuno\\qualcosa", ["disperdere"], ACTV),
        OrdinarySemRole("dei giovani manifestanti", ["disperdere"], PASSV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test23(tagger):
    result = tagger.tag(
        "Le autorità hanno interrotto la manifestazione contro il razzismo perché questi giovani hanno rotto delle vetrate lanciando sampietrini"
    )
    actual_sem_roles: List[Tag] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("Le autorità", ["interrompere"], ACTV),
        OrdinarySemRole("la manifestazione", ["interrompere"], PASSV),
        OrdinarySemRole("questi giovani", ["rompere"], ACTV),
        OrdinarySemRole("delle vetrate", ["rompere"], "ACTIVE_SI"),
        OrdinarySemRole("qualcuno\\qualcosa", ["lanciare"], ACTV),
        OrdinarySemRole("sampietrini", ["lanciare"], PASSV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test25(tagger):
    result = tagger.tag("Le immagini viste in TV hanno scioccato gli Italiani")
    actual_sem_roles: List[Tag] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("Le immagini viste", ["scioccare"], ACTV),
        OrdinarySemRole("Le immagini", ["vedere"], PASSV),
        OrdinarySemRole("gli Italiani", ["scioccare"], PASSV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test26(tagger):
    result = tagger.tag(
        "I manifestanti hanno anche violato delle regole imposte dal Covid"
    )
    actual_sem_roles: List[Tag] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("I manifestanti", ["violare"], ACTV),
        OrdinarySemRole("delle regole imposte", ["violare"], PASSV),
        OrdinarySemRole("delle regole", ["imporre"], PASSV),
        OrdinarySemRole("il covid", ["imporre"], ACTV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test27(tagger):  # v. test 16
    result = tagger.tag("Marco si è consegnato")
    actual_sem_roles: List[Tag] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("marco", ["consegnare"], ACTV),
        OrdinarySemRole("marco", ["consegnare"], PASSV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test28(tagger):
    result = tagger.tag(
        "Un brigadiere della Guardia di Finanza che davanti al giudice non ha ammesso le proprie responsabilità"
    )
    actual_sem_roles: List[Tag] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("un brigadiere", ["ammettere"], ACTV, neg=True),
        OrdinarySemRole("le proprie responsabilità", ["ammettere"], PASSV, neg=True),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test28_(tagger):
    result = tagger.tag(
        "Un brigadiere della Guardia di Finanza che davanti al giudice ha ammesso le proprie responsabilità"
    )
    actual_sem_roles: List[Tag] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("un brigadiere", ["ammettere"], ACTV),
        OrdinarySemRole("le proprie responsabilità", ["ammettere"], PASSV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test29(tagger):
    result = tagger.tag("Non sono stati pubblicati ulteriori dettagli")
    actual_sem_roles: List[Tag] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("ulteriori dettagli", ["pubblicare"], PASSV, neg=True)
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test30(tagger):
    result = tagger.tag("Pietro vede l'occasione giusta per attaccare l'Alleanza")
    actual_sem_roles: List[Tag] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("Pietro", ["vedere"], ACTV),
        OrdinarySemRole("l'occasione giusta", ["vedere"], PASSV),
        OrdinarySemRole("l'Alleanza", ["attaccare"], PASSV),
        OrdinarySemRole("QUALCUNO\\QUALCOSA", ["attaccare"], ACTV),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test31(tagger):
    result = tagger.tag("Giulio lo dice poi a Patrizia")
    actual_sem_roles: List[Tag] = result["sem_roles"]
    expected_sem_roles = [
        OrdinarySemRole("Giulio", ["dire"], ACTV),
        OrdinarySemRole("lo", ["dire"], PASSV),
        DativeSemRole("Patrizia", ["dire"]),
    ]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)


def test32(tagger):
    result = tagger.tag(
        "Per quella vicenda il maresciallo capo dei carabinieri Pasquale Nastri,"
        " 57 anni, all’epoca vice comandante della stazione di Marsala, nel 2016 "
        "era stato condannato per concussione"
    )
    actual_sem_roles: List[Tag] = result["sem_roles"]
    expected_sem_roles = [OrdinarySemRole("il maresciallo capo", ["condannare"], PASSV)]
    list_equals_no_order(actual_sem_roles, expected_sem_roles)
