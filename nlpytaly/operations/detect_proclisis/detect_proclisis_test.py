from typing import List

import pytest

from nlpytaly import NLPYTALY
from nlpytaly.Tag import Tag


@pytest.fixture()
def tagger():
    return NLPYTALY()


def test1(tagger):
    result = tagger.tag("Non ho capito se se ne è accorto.")
    tags: List[Tag] = result["tags"]
    assert [t.block for t in tags] == [1, 1, 1, 2, 3, 3, 3, 3, 4]
    assert tags[3].pos == "CON"
    assert tags[4].pos == "CLIT"


def test2(tagger):
    result = tagger.tag("Se ne è accorto.")
    tags: List[Tag] = result["tags"]
    assert [t.block for t in tags] == [1, 1, 1, 1, 2]
    assert tags[0].pos == "CLIT"


def test3(tagger):
    result = tagger.tag("Non me lo si è dato")
    tags: List[Tag] = result["tags"]
    assert tags[0].is_proclisis is True
    assert tags[1].is_proclisis is True
    assert tags[2].is_proclisis is True
    assert tags[3].is_proclisis is True


def test4(tagger):
    result = tagger.tag("A me servono delle penne")
    tags: List[Tag] = result["tags"]
    assert tags[0].is_proclisis is None
    assert tags[1].is_proclisis is None


@pytest.mark.skip
def test5(tagger):
    result = tagger.tag("A me mi servono delle penne")
    tags: List[Tag] = result["tags"]
    assert tags[0].is_proclisis is None
    assert tags[1].is_proclisis is None
    assert tags[2].is_proclisis is True
