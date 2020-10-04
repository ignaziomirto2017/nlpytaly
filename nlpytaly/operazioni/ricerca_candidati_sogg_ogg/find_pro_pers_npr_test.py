import pytest

from nlpytaly import nlpytaly


@pytest.fixture()
def tagger():
    return nlpytaly()


def test1(tagger):
    tagger.tag("John Wayne si è fatto la barba")
    tags = tagger.tags
    assert [t.block for t in tags] == [1, 1, 2, 2, 2, 3, 3]
    assert tags[0].ruolo_sintattico == "SOGG"
    assert tags[1].ruolo_sintattico == "SOGG"


def test2(tagger):
    tagger.tag("Mario Draghi valuta ulteriori aiuti alle banche europee.")
    tags = tagger.tags
    assert [t.block for t in tags] == [1, 1, 2, 3, 3, 3, 3, 3, 3]
    assert tags[0].ruolo_sintattico == "SOGG"
    assert tags[1].ruolo_sintattico == "SOGG"
