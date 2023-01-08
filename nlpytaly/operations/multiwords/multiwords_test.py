import pytest

from nlpytaly import NLPYTALY

from .multiwords import _lemma


@pytest.fixture()
def tagger():
    return NLPYTALY()


def test1(tagger):
    tagger.tag("L'intervento ha fatto lamentare il paziente a lungo")
    tags = tagger.tags
    assert [t.block for t in tags] == [1, 1, 2, 2, 2, 3, 3, 4]
    assert tags[-1].lemma == _lemma
    assert tags[-1].occurrence == "a lungo"


def test2(tagger):
    tagger.tag("L'intervento ha fatto lamentare il paziente di punto in bianco")
    tags = tagger.tags
    assert [t.block for t in tags] == [1, 1, 2, 2, 2, 3, 3, 4]
    assert tags[-1].lemma == _lemma
    assert tags[-1].occurrence == "di punto in bianco"
