import pytest

from nlpytaly import NLPYTALY


@pytest.fixture()
def tagger():
    return NLPYTALY()


def test1(tagger):
    tagger.tag("John Wayne si è fatto la barba")
    tags = tagger.tags
    assert [t.block for t in tags] == [1, 1, 2, 2, 2, 3, 3]
    assert tags[0].syntactic_role == "SOGG"
    assert tags[1].syntactic_role == "SOGG"


def test2(tagger):
    tagger.tag("Mario Draghi valuta ulteriori aiuti alle banche europee")
    tags = tagger.tags
    assert [t.block for t in tags] == [1, 1, 2, 3, 3, 4, 4, 4]
    assert tags[0].syntactic_role == "SOGG"
    assert tags[1].syntactic_role == "SOGG"


def test3(tagger):
    tagger.tag("La relazione con la bella Maria sta naufragando")
    tags = tagger.tags
    assert [t.block for t in tags] == [1, 1, 2, 2, 2, 2, 3, 3]
    assert tags[0].syntactic_role == "SOGG"
    assert tags[1].syntactic_role == "SOGG"
