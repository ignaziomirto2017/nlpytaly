import pytest

from nlpytaly import nlpytaly


@pytest.fixture()
def tagger():
    return nlpytaly()


def test1(tagger):
    tagger.tag(
        "Noi siamo partiti quando Gianni era a casa. Noi ci siamo divertiti molto."
    )
    tags = tagger.tags
    assert [t.block for t in tags] == [1, 2, 2, 2, 3, 4, 5, 5, 5, 6, 7, 7, 7, 7, 8]


def test2(tagger):
    tagger.tag("Le maestre prendono a bacchettate gli alunni.")
    tags = tagger.tags
    assert [t.block for t in tags] == [1, 1, 2, 3, 3, 4, 4, 5]
