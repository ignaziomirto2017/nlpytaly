import pytest

from nlpytaly import NLPYTALY


@pytest.fixture()
def tagger():
    return NLPYTALY()


def test1(tagger):
    tagger.tag("Mi sono scocciato")
    tags = tagger.tags
    assert tags[1].person == "1st"
    assert tags[1].number == "s"


def test2(tagger):
    tagger.tag("Si sono scocciati")
    tags = tagger.tags
    assert tags[1].person == "3rd"
    assert tags[1].number == "p"


def test3(tagger):
    tagger.tag("Mi sono concesse")
    tags = tagger.tags
    assert tags[1].person == "3rd"
    assert tags[1].number == "p"


def test4(tagger):
    tagger.tag("Sono emerse delle perplessità")
    tags = tagger.tags
    assert tags[0].person == "3rd"
    assert tags[0].number == "p"
