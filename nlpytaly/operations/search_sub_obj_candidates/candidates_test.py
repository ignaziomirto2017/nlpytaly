from typing import List

import pytest

from nlpytaly import NLPYTALY

from ...Tag import Tag


def get_true_values(tags: List[Tag]):
    return list(
        map(
            lambda x: x[0],
            filter(lambda x: x[1], enumerate([t._is_sub_obj_candidate for t in tags])),
        )
    )


@pytest.fixture()
def tagger():
    return NLPYTALY()


def test1(tagger):
    tagger.tag("L'uomo biondo gioca a tennis")
    tags: List[Tag] = tagger.tags
    assert get_true_values(tags) == [0, 1, 2]


def test2(tagger):
    tagger.tag("Lo stanco amico gioca a tennis")
    tags: List[Tag] = tagger.tags
    assert get_true_values(tags) == [0, 1, 2]


def test3(tagger):
    tagger.tag("Ho visto quelle strane persone giocare a tennis")
    tags: List[Tag] = tagger.tags
    assert get_true_values(tags) == [2, 3, 4]


@pytest.mark.skip
def test4(tagger):
    tagger.tag("Furono messi in azione i migliori agenti segreti")
    tags: List[Tag] = tagger.tags
    assert get_true_values(tags) == [4, 5, 6, 7]


def test5(tagger):
    tagger.tag("Ho visto quelle strane persone giocare a tennis")
    tags: List[Tag] = tagger.tags
    assert get_true_values(tags) == [2, 3, 4]


def test6(tagger):
    tagger.tag("Mario ha visto te")
    tags: List[Tag] = tagger.tags
    assert get_true_values(tags) == [0, 3]


def test7(tagger):
    tagger.tag("Mario ha fatto la barba a Luigi")  # Meronymy
    tags: List[Tag] = tagger.tags
    assert get_true_values(tags) == [0, 3, 4]


def test8(tagger):
    tagger.tag("Il marito Oliver indaga")
    tags: List[Tag] = tagger.tags
    assert get_true_values(tags) == [0, 1, 2]


def test9(tagger):
    tagger.tag("Mia zia viaggia")
    tags: List[Tag] = tagger.tags
    assert get_true_values(tags) == [0, 1]


def test10(tagger):
    tagger.tag("Mangiamo patate")
    tags: List[Tag] = tagger.tags
    assert get_true_values(tags) == [1]


def test11(tagger):
    tagger.tag("Mio nipote pettina Giovanna")
    tags: List[Tag] = tagger.tags
    assert get_true_values(tags) == [0, 1, 3]
    assert tags[1].gender == "m"
    assert tags[1].number == "s"


def test12(tagger):
    tagger.tag("Mia nipote pettina Giovanna")
    tags: List[Tag] = tagger.tags
    assert get_true_values(tags) == [0, 1, 3]
    assert tags[1].gender == "f"
    assert tags[1].number == "s"


def test13(tagger):
    tagger.tag(
        "Farà conoscere tramite i suoi canali social, altri tre muri dove ha pubblicato suoi lavori"
    )
    tags: List[Tag] = tagger.tags
    assert get_true_values(tags) == [8, 9, 10, 14, 15]


def test14(tagger):
    tagger.tag("Mario prova odio per la politica")
    tags: List[Tag] = tagger.tags
    assert get_true_values(tags) == [0, 2]


def test15(tagger):
    tagger.tag("Io ho visto 4 simpatici amici")
    tags: List[Tag] = tagger.tags
    assert get_true_values(tags) == [0, 3, 4, 5]


def test16(tagger):
    tagger.tag("Io ho visto quattro simpatici amici")
    tags: List[Tag] = tagger.tags
    assert get_true_values(tags) == [0, 3, 4, 5]


def test17(tagger):
    tagger.tag("Mario ha fatto comprare l'orologio a un suo amico")
    tags: List[Tag] = tagger.tags
    assert get_true_values(tags) == [0, 4, 5]


def test18(tagger):
    tagger.tag("Mio cugino è partito")
    tags: List[Tag] = tagger.tags
    assert get_true_values(tags) == [0, 1]
