import pytest

from nlpytaly import nlpytaly


@pytest.fixture()
def tagger():
    return nlpytaly()


def test1(tagger):
    tagger.tag("Consegna la merce")
    tags = tagger.tags
    assert tags[0].is_inflected_verb()


def test2(tagger):
    tagger.tag("La consegna della merce fu lenta")
    tags = tagger.tags
    assert tags[1].is_noun()


def test3(tagger):
    tagger.tag("Appoggi la sedia")
    tags = tagger.tags
    assert tags[0].is_inflected_verb()


def test4(tagger):
    tagger.tag("Danno la recita")
    tags = tagger.tags
    assert tags[0].is_inflected_verb()


def test5(tagger):
    tagger.tag("Tu appoggi la sedia")
    tags = tagger.tags
    assert tags[1].is_inflected_verb()


def test6(tagger):
    tagger.tag("Ho fatto danno ")
    tags = tagger.tags
    assert tags[-1].is_noun()
