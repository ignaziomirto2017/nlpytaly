from typing import List

import pytest

from nlpytaly import nlpytaly
from ...Tag import Tag


def get_true_values(tags: List["Tag"]):
    return list(
        map(
            lambda x: x[0],
            filter(lambda x: x[1], enumerate([t.is_candidate for t in tags])),
        )
    )


@pytest.fixture()
def tagger():
    return nlpytaly()


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
    tagger.tag("Mario ha fatto la barba a Luigi")
    tags: List[Tag] = tagger.tags
    assert get_true_values(tags) == [0, 3, 4]


def test8(tagger):
    tagger.tag("Il marito Oliver indaga")
    tags: List[Tag] = tagger.tags
    assert get_true_values(tags) == [0, 1, 2]
