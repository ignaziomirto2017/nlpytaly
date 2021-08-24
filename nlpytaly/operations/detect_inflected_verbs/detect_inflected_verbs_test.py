from typing import List

import pytest

from nlpytaly import NLPYTALY
from ...Tag import Tag


def get_true_values(tags):
    return list(
        map(
            lambda x: x[0],
            filter(lambda x: x[1], enumerate([t._is_inflected_verb for t in tags])),
        )
    )


@pytest.fixture()
def tagger():
    return NLPYTALY()


def test1(tagger):
    result = tagger.tag("Gli alunni uccidono la maestra.")
    tags: List[Tag] = result["tags"]
    assert get_true_values(tags) == [2]


def test2(tagger):
    result = tagger.tag("Gli alunni hanno mangiato la maestra.")
    tags: List[Tag] = result["tags"]
    assert get_true_values(tags) == [2, 3]


def test3(tagger):
    result = tagger.tag("Gli alunni hanno mangiato spesso la maestra.")
    tags: List[Tag] = result["tags"]
    assert get_true_values(tags) == [2, 3, 4]


def test3_neg(tagger):
    result = tagger.tag("Gli alunni non hanno mangiato spesso la maestra.")
    tags: List[Tag] = result["tags"]
    assert get_true_values(tags) == [2, 3, 4, 5]


def test4(tagger):
    result = tagger.tag("Mario non parla")
    tags: List[Tag] = result["tags"]
    assert get_true_values(tags) == [1, 2]


def test5(tagger):
    result = tagger.tag("Vado spesso al mare di domenica.")
    tags: List[Tag] = result["tags"]
    assert get_true_values(tags) == [0, 1]


def test6(tagger):
    result = tagger.tag("Mario è insegnante")
    tags: List[Tag] = result["tags"]
    assert [t.block for t in tags] == [1, 2, 3]
    assert tags[1].is_main_verb()


def test7(tagger):
    result = tagger.tag("è stato insegnante")
    tags: List[Tag] = result["tags"]
    assert [t.block for t in tags] == [1, 1, 2]
    assert tags[0].is_aux()


def test8(tagger):
    result = tagger.tag("Lui ha giocato spesso a pallone")
    tags: List[Tag] = result["tags"]
    assert [t.block for t in tags] == [1, 2, 2, 2, 3, 3]
    assert tags[1].is_aux()
