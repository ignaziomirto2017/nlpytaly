import pytest

from nlpytaly import nlpytaly


@pytest.fixture()
def tagger():
    return nlpytaly()


def test1(tagger):
    tagger.tag("Le foto non le erano ancora state fatte dal marito")
    tags = tagger.tags

    # testa il blocco
    assert [t.block for t in tags] == [1, 1, 2, 2, 2, 2, 2, 2, 3, 3]

    # testa la diatesi
    for t in tags:
        if t.block == 2:
            assert t.is_passive()

    # testa le funzioni sintattiche (SOGG, OD, PN)
    assert tags[0].ruolo_sintattico == "SOGG"
    assert tags[1].ruolo_sintattico == "SOGG"


def test2(tagger):
    tagger.tag("Mario gioca")
    tags = tagger.tags

    # testa il blocco
    assert [t.block for t in tags] == [1, 2]

    # testa la diatesi
    for t in tags:
        if t.block == 2:
            assert t.is_active()

    # testa le funzioni sintattiche (SOGG, OD, PN)
    assert tags[0].ruolo_sintattico == "SOGG"


def test3(tagger):
    tagger.tag(
        "Gli studenti stranieri hanno preso le piccole pecorelle a sassate per colpire i vicini"
    )
    tags = tagger.tags

    # testa il blocco
    assert [t.block for t in tags] == [1, 1, 1, 2, 2, 3, 3, 3, 4, 4, 5, 5, 6, 6]

    # testa la diatesi
    for t in tags:
        if t.block == 2:
            assert t.is_active()

    # testa le funzioni sintattiche (SOGG, OD, PN)
    assert tags[0].ruolo_sintattico == "SOGG"
    assert tags[1].ruolo_sintattico == "SOGG"
    assert tags[5].ruolo_sintattico == "OD"
    assert tags[6].ruolo_sintattico == "OD"
    assert tags[7].ruolo_sintattico == "OD"
    assert tags[12].ruolo_sintattico == "OD"
    assert tags[13].ruolo_sintattico == "OD"


def test4(tagger):
    tagger.tag("Fioccano le multe")
    tags = tagger.tags

    # testa il blocco
    assert [t.block for t in tags] == [1, 2, 2]

    # testa la diatesi
    for t in tags:
        if t.block == 1:
            assert t.is_middle_mr()

    # testa le funzioni sintattiche (SOGG, OD, PN)
    assert tags[1].ruolo_sintattico == "SOGG"
    assert tags[2].ruolo_sintattico == "SOGG"


def test5(tagger):
    tagger.tag("I gatti si sono sempre spaventati dei cani")
    tags = tagger.tags

    # testa il blocco
    assert [t.block for t in tags] == [1, 1, 2, 2, 2, 2, 3, 3]

    # testa la diatesi
    for t in tags:
        if t.block == 2:
            assert t.is_middle_pr()
    assert tags[2].diathesis == "MIDDLE_PR"

    # testa le funzioni sintattiche (SOGG, OD, PN)
    assert tags[0].ruolo_sintattico == "SOGG"
    assert tags[1].ruolo_sintattico == "SOGG"


def test6(tagger):
    tagger.tag("Quelle obiezioni furono mosse dalle donne al capo")
    tags = tagger.tags

    # testa il blocco
    assert [t.block for t in tags] == [1, 1, 2, 2, 3, 3, 3, 3]

    # testa la diatesi
    for t in tags:
        if t.block == 2:
            assert t.is_passive()
    assert tags[2].diathesis == "PASSIVE"

    # testa le funzioni sintattiche (SOGG, OD, PN)
    assert tags[0].ruolo_sintattico == "SOGG"
    assert tags[1].ruolo_sintattico == "SOGG"
    assert tags[2].note == "AUX"


def test7(tagger):
    tagger.tag("Quel denaro è stato messo a rischio dagli investitori")
    tags = tagger.tags

    # testa il blocco
    assert [t.block for t in tags] == [1, 1, 2, 2, 2, 3, 3, 3, 3]

    # testa la diatesi
    for t in tags:
        if t.block == 2:
            assert t.is_passive()
    assert tags[2].diathesis == "PASSIVE"

    # testa le funzioni sintattiche (SOGG, OD, PN)
    assert tags[0].ruolo_sintattico == "SOGG"
    assert tags[1].ruolo_sintattico == "SOGG"
    assert tags[2].note == "AUX"


def test8(tagger):
    tagger.tag("Il nostro amico ha preso appuntamento col medico")
    tags = tagger.tags

    # testa il blocco
    assert [t.block for t in tags] == [1, 1, 1, 2, 2, 3, 3, 3]

    # testa la diatesi
    for t in tags:
        if t.block == 2:
            assert t.is_active()
    assert tags[3].diathesis == "ACTIVE"
    assert tags[4].diathesis == "ACTIVE"

    # testa le funzioni sintattiche (SOGG, OD, PN)
    assert tags[0].ruolo_sintattico == "SOGG"
    assert tags[1].ruolo_sintattico == "SOGG"
    assert tags[2].ruolo_sintattico == "SOGG"
    assert tags[3].note == "AUX"


def test9(tagger):
    tagger.tag("La cortesia è stata fatta da Gianni")
    tags = tagger.tags

    # testa il blocco
    assert [t.block for t in tags] == [1, 1, 2, 2, 2, 3, 3]

    # testa la diatesi
    for t in tags:
        if t.block == 2:
            assert t.is_passive()
    assert tags[3].diathesis == "PASSIVE"
    assert tags[4].diathesis == "PASSIVE"

    # testa le funzioni sintattiche (SOGG, OD, PN)
    assert tags[0].ruolo_sintattico == "SOGG"
    assert tags[1].ruolo_sintattico == "SOGG"
    assert tags[2].note == "AUX"


def test10(tagger,):
    tagger.tag(
        "Le audizioni pubblicate in questa sede contribuiscono a ricostruire una complessa questione"
    )
    tags = tagger.tags

    # testa il blocco
    assert [t.block for t in tags] == [1, 1, 1, 2, 2, 2, 3, 4, 4, 5, 5, 5]

    # testa la diatesi
    for t in tags:
        if t.block == 3:
            assert t.is_active()
    assert tags[6].diathesis == "ACTIVE"

    # testa le funzioni sintattiche (SOGG, OD, PN)
    assert tags[0].ruolo_sintattico == "SOGG"
    assert tags[1].ruolo_sintattico == "SOGG"
    assert tags[2].ruolo_sintattico == "SOGG"
    assert tags[9].ruolo_sintattico == "OD"
    assert tags[10].ruolo_sintattico == "OD"
    assert tags[11].ruolo_sintattico == "OD"
    assert tags[6].note == "Main verb"


def test11(tagger):
    tagger.tag("Oggi mi sono concessi")
    tags = tagger.tags

    # testa il blocco
    assert [t.block for t in tags] == [1, 2, 2, 2]

    # testa la diatesi
    for t in tags:
        if t.block == 2:
            assert t.is_passive()
    assert tags[1].diathesis == "PASSIVE"
    assert tags[2].diathesis == "PASSIVE"
    assert tags[3].diathesis == "PASSIVE"
    assert tags[2].note == "AUX"


def test12(tagger):
    tagger.tag("Oggi mi sono concesso")
    tags = tagger.tags

    # testa il blocco
    assert [t.block for t in tags] == [1, 2, 2, 2]

    # testa la diatesi
    for t in tags:
        if t.block == 2:
            assert t.is_middle_pr()
    assert tags[1].diathesis == "MIDDLE_PR"
    assert tags[2].diathesis == "MIDDLE_PR"
    assert tags[3].diathesis == "MIDDLE_PR"
    assert tags[2].note == "AUX"


def test13(tagger):
    tagger.tag("Gli inquirenti hanno messo gli investigatori alla ricerca del denaro")
    tags = tagger.tags

    # testa il blocco
    assert [t.block for t in tags] == [1, 1, 2, 2, 3, 3, 4, 4, 4, 4]

    # testa la diatesi
    for t in tags:
        if t.block == 2:
            assert t.is_active()
    assert tags[2].diathesis == "ACTIVE"
    assert tags[3].diathesis == "ACTIVE"
    assert tags[2].note == "AUX"
    assert tags[0].ruolo_sintattico == "SOGG"
    assert tags[1].ruolo_sintattico == "SOGG"
    assert tags[4].ruolo_sintattico == "OD"
    assert tags[5].ruolo_sintattico == "OD"


def test14(tagger):
    tagger.tag("Leo ha fatto colpo in banca")
    tags = tagger.tags

    # testa il blocco
    assert [t.block for t in tags] == [1, 2, 2, 3, 3, 3]

    # testa la diatesi
    for t in tags:
        if t.block == 2:
            assert t.is_active()
    assert tags[1].diathesis == "ACTIVE"
    assert tags[2].diathesis == "ACTIVE"
    assert tags[1].note == "AUX"
    assert tags[0].ruolo_sintattico == "SOGG"


def test15(tagger):
    tagger.tag("Leo ha fatto un colpo in banca")
    tags = tagger.tags

    # testa il blocco
    assert [t.block for t in tags] == [1, 2, 2, 3, 3, 4, 4]

    # testa la diatesi
    for t in tags:
        if t.block == 2:
            assert t.is_active()
    assert tags[1].diathesis == "ACTIVE"
    assert tags[2].diathesis == "ACTIVE"
    assert tags[1].note == "AUX"
    assert tags[0].ruolo_sintattico == "SOGG"


def test16(tagger):
    tagger.tag("Lui è un medico scozzese")
    tags = tagger.tags

    # testa il blocco
    assert [t.block for t in tags] == [1, 2, 3, 3, 3]

    # testa la diatesi
    for t in tags:
        if t.block == 2:
            assert t.is_middle_mr()
    assert tags[1].diathesis == "MIDDLE_MR"
    assert tags[1].note == "Main verb"
    assert tags[0].ruolo_sintattico == "SOGG"
    assert tags[2].ruolo_sintattico == "PN"
    assert tags[3].ruolo_sintattico == "PN"
    assert tags[4].ruolo_sintattico == "PN"


def test17(tagger):
    tagger.tag("Oggi la politica è diventata un salotto di comunicazione")
    tags = tagger.tags

    # testa il blocco
    assert [t.block for t in tags] == [1, 2, 2, 3, 3, 4, 4, 5, 5]

    # testa la diatesi
    for t in tags:
        if t.block == 3:
            assert t.is_middle_mr()
    assert tags[3].diathesis == "MIDDLE_MR"
    assert tags[4].diathesis == "MIDDLE_MR"
    assert tags[3].note == "AUX"
    assert tags[1].ruolo_sintattico == "SOGG"
    assert tags[2].ruolo_sintattico == "SOGG"
    assert tags[5].ruolo_sintattico == "PN"
    assert tags[6].ruolo_sintattico == "PN"


def test18(tagger):
    tagger.tag(
        "Un serial killer con disturbi mentali ha compiuto una strage in un motel per dimenticare il lutto"
    )
    tags = tagger.tags

    # testa il blocco
    assert [t.block for t in tags] == [
        1,
        1,
        1,
        2,
        2,
        2,
        3,
        3,
        4,
        4,
        5,
        5,
        5,
        6,
        6,
        7,
        7,
    ]

    # testa la diatesi
    for t in tags:
        if t.block == 3:
            assert t.is_active()
    assert tags[6].diathesis == "ACTIVE"
    assert tags[7].diathesis == "ACTIVE"
    assert tags[6].note == "AUX"
    assert tags[0].ruolo_sintattico == "SOGG"
    assert tags[1].ruolo_sintattico == "SOGG"
    assert tags[2].ruolo_sintattico == "SOGG"
    assert tags[8].ruolo_sintattico == "OD"
    assert tags[9].ruolo_sintattico == "OD"
    assert tags[15].ruolo_sintattico == "OD"
    assert tags[16].ruolo_sintattico == "OD"


def test19(tagger):
    tagger.tag("Mi faccio una scappata a Roma")
    tags = tagger.tags

    # testa il blocco
    assert [t.block for t in tags] == [1, 1, 2, 2, 3, 3]

    # testa la diatesi
    for t in tags:
        if t.block == 1:
            assert t.is_middle_pr()
    assert tags[0].diathesis == "MIDDLE_PR"
    assert tags[1].diathesis == "MIDDLE_PR"
    assert tags[1].note == "Main verb"
    assert tags[2].ruolo_sintattico == "OD"
    assert tags[3].ruolo_sintattico == "OD"


def test20(tagger):
    tagger.tag("Vogliono degli studenti")
    tags = tagger.tags

    # testa il blocco
    assert [t.block for t in tags] == [1, 2, 2]

    # testa la diatesi
    for t in tags:
        if t.block == 1:
            assert t.is_active()
    assert tags[0].diathesis == "ACTIVE"
    assert tags[0].note == "Main verb"
    assert tags[1].ruolo_sintattico == "SOGG|OD"
    assert tags[2].ruolo_sintattico == "SOGG|OD"


def test21(tagger):
    tagger.tag("Ci vogliono degli studenti")
    tags = tagger.tags

    # testa il blocco
    assert [t.block for t in tags] == [1, 1, 2, 2]

    # testa la diatesi
    for t in tags:
        if t.block == 1:
            assert t.is_middle_mr()
    assert tags[0].diathesis == "MIDDLE_MR"
    assert tags[1].diathesis == "MIDDLE_MR"
    assert tags[1].note == "Main verb"
    assert tags[2].ruolo_sintattico == "SOGG"
    assert tags[3].ruolo_sintattico == "SOGG"
