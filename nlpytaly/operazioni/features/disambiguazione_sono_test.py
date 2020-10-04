import pytest

from nlpytaly import nlpytaly


@pytest.fixture()
def tagger():
    return nlpytaly()


def test1(tagger):
    tagger.tag("Mi sono scocciato")
    tags = tagger.tags
    assert tags[1].persona == "1st"
    assert tags[1].numero == "s"


def test2(tagger):
    tagger.tag("Si sono scocciati")
    tags = tagger.tags
    assert tags[1].persona == "3rd"
    assert tags[1].numero == "p"


def test3(tagger):
    tagger.tag("Mi sono concesse")
    tags = tagger.tags
    assert tags[1].persona == "3rd"
    assert tags[1].numero == "p"


def test4(tagger):
    tagger.tag("Sono emerse delle perplessità")
    tags = tagger.tags
    assert tags[0].persona == "3rd"
    assert tags[0].numero == "p"
