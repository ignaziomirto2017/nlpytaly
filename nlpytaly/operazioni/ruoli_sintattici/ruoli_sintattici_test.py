from typing import List

import pytest

from nlpytaly import nlpytaly
from nlpytaly.Tag import Tag


@pytest.fixture()
def tagger():
    return nlpytaly()


def test1(tagger):
    result = tagger.tag("Gli alunni uccidono la maestra.")
    tags: List[Tag] = result["tags"]
    assert tags[0].ruolo_sintattico == "SOGG"
    assert tags[1].ruolo_sintattico == "SOGG"
    assert tags[3].ruolo_sintattico == "OD"
    assert tags[4].ruolo_sintattico == "OD"


def test2(tagger):
    result = tagger.tag("Lei uccide il tempo.")
    tags: List[Tag] = result["tags"]
    assert tags[0].ruolo_sintattico == "SOGG"
    assert tags[2].ruolo_sintattico == "OD"
    assert tags[3].ruolo_sintattico == "OD"


def test4(tagger):
    result = tagger.tag("I ragazzi giocano a pallone")
    tags: List[Tag] = result["tags"]
    assert tags[0].ruolo_sintattico == "SOGG"
    assert tags[1].ruolo_sintattico == "SOGG"


def test5(tagger):
    result = tagger.tag("Siamo andati a Milano per comprare le mele")
    tags: List[Tag] = result["tags"]
    assert tags[6].ruolo_sintattico == "OD"
    assert tags[7].ruolo_sintattico == "OD"


def test6(tagger):
    result = tagger.tag("Noi siamo andati a Milano per comprare le mele")
    tags: List[Tag] = result["tags"]
    assert tags[0].ruolo_sintattico == "SOGG"
    assert tags[7].ruolo_sintattico == "OD"
    assert tags[8].ruolo_sintattico == "OD"


def test7(tagger):
    result = tagger.tag("Si mise l'uomo sotto controllo")
    tags: List[Tag] = result["tags"]
    assert tags[2].ruolo_sintattico == "SOGG"
    assert tags[3].ruolo_sintattico == "SOGG"


def test8(tagger):
    result = tagger.tag("Nanni è uno squilibrato")
    tags: List[Tag] = result["tags"]
    assert tags[0].ruolo_sintattico == "SOGG"
    assert tags[2].ruolo_sintattico == "PN"
    assert tags[3].ruolo_sintattico == "PN"


def test9(tagger):
    result = tagger.tag("Il ricercato diventò uno squilibrato")
    tags: List[Tag] = result["tags"]
    assert tags[0].ruolo_sintattico == "SOGG"
    assert tags[1].ruolo_sintattico == "SOGG"
    assert tags[3].ruolo_sintattico == "PN"
    assert tags[4].ruolo_sintattico == "PN"


def test10(tagger):
    result = tagger.tag("Le maestre prendono a bacchettate gli alunni")
    tags: List[Tag] = result["tags"]
    assert tags[0].ruolo_sintattico == "SOGG"
    assert tags[1].ruolo_sintattico == "SOGG"
    assert tags[-1].ruolo_sintattico == "OD"
    assert tags[-2].ruolo_sintattico == "OD"


def test11(tagger):
    result = tagger.tag("Le maestre prendono gli alunni a bacchettate")
    tags: List[Tag] = result["tags"]
    assert tags[0].ruolo_sintattico == "SOGG"
    assert tags[1].ruolo_sintattico == "SOGG"
    assert tags[3].ruolo_sintattico == "OD"
    assert tags[4].ruolo_sintattico == "OD"


def test12(tagger):
    result = tagger.tag("Sorride Mario")
    tags: List[Tag] = result["tags"]
    assert tags[1].ruolo_sintattico == "SOGG"

    result = tagger.tag("Ha sorriso Mario")
    tags: List[Tag] = result["tags"]
    assert tags[2].ruolo_sintattico == "SOGG"

    result = tagger.tag("Viene Mario")
    tags: List[Tag] = result["tags"]
    assert tags[1].ruolo_sintattico == "SOGG"

    result = tagger.tag("è venuto Mario")
    tags: List[Tag] = result["tags"]
    assert tags[2].ruolo_sintattico == "SOGG"


def test13(tagger):
    result = tagger.tag("Luigi fa il meccanico")
    tags: List[Tag] = result["tags"]
    assert tags[0].ruolo_sintattico == "SOGG"
    assert tags[3].ruolo_sintattico is None


def test14(tagger):
    result = tagger.tag("Luigi è uscito per comprare il pane")
    tags: List[Tag] = result["tags"]
    assert tags[0].ruolo_sintattico == "SOGG"
    assert tags[5].ruolo_sintattico == "OD"
    assert tags[6].ruolo_sintattico == "OD"


def test15(tagger):
    result = tagger.tag("Comprando il pane, Luigi si è fatto male")
    tags: List[Tag] = result["tags"]
    assert tags[1].ruolo_sintattico == "OD"
    assert tags[2].ruolo_sintattico == "OD"
    assert tags[4].ruolo_sintattico == "SOGG"


def test16(tagger):
    result = tagger.tag("Il magistrato fu deferito per non avere accusato il teste")
    tags: List[Tag] = result["tags"]
    assert tags[0].ruolo_sintattico == "SOGG"
    assert tags[1].ruolo_sintattico == "SOGG"

    assert tags[8].ruolo_sintattico == "OD"
    assert tags[9].ruolo_sintattico == "OD"
