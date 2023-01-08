import pytest

from nlpytaly import NLPYTALY


@pytest.fixture()
def tagger():
    return NLPYTALY()


def test1(tagger):
    tagger.tag("I cani spaventano dei gatti")
    tags = tagger.tags
    assert [t.block for t in tags] == [1, 1, 2, 3, 3]
    assert tags[-2].pos == "DET:part"


def test2(tagger):
    tagger.tag("Noi diventeremo degli amici")
    tags = tagger.tags
    assert [t.block for t in tags] == [1, 2, 3, 3]
    assert tags[-2].pos == "DET:part"
    assert tags[-1]._syntactic_role == "PN"


@pytest.mark.skip
def test_s(tagger):
    tagger.tag("Diventeremo degli uomini")
    tags = tagger.tags
    assert [t.block for t in tags] == [1, 2, 2]
    assert tags[-2].pos == "DET:part"
    assert tags[-1]._syntactic_role == "PN"


def test3(tagger):
    tagger.tag("Ci sono degli studenti qui")
    tags = tagger.tags
    assert [t.block for t in tags] == [1, 1, 2, 2, 3]
    assert tags[-3].pos == "DET:part"


def test4(tagger):
    tagger.tag("Preoccupi dei professori")
    tags = tagger.tags
    assert [t.block for t in tags] == [1, 2, 2]
    assert tags[-2].pos == "DET:part"


@pytest.mark.skip
def test5(tagger):
    tagger.tag("Ti preoccupi dei professori")
    tags = tagger.tags
    assert [t.block for t in tags] == [1, 1, 2, 2]
    assert tags[-2].pos == "PRE:det"


def test6(tagger):
    tagger.tag("Ci sono stati degli incovenienti qui")
    tags = tagger.tags
    assert [t.block for t in tags] == [1, 1, 1, 2, 2, 3]
    assert tags[-3].pos == "DET:part"


def test7(tagger):
    tagger.tag("Sono stupito dei colleghi stranieri")
    tags = tagger.tags
    assert [t.block for t in tags] == [1, 1, 2, 2, 2]
    assert tags[-3].pos == "PRE:det"


def test8(tagger):
    tagger.tag("Degli ingegneri hanno fatto delle accurate valutazioni dei dati")
    tags = tagger.tags
    assert [t.block for t in tags] == [1, 1, 2, 2, 3, 3, 3, 3, 3]
    assert tags[-2].pos == "PRE:det"
    assert tags[-5].pos == "DET:part"
    assert tags[0].pos == "DET:part"


def test81(tagger):
    tagger.tag("Degli ingegneri arrivano")
    tags = tagger.tags
    assert [t.block for t in tags] == [1, 1, 2]
    assert tags[0].pos == "DET:part"


def test82(tagger):
    tagger.tag("Degli ingegneri sono arrivati")
    tags = tagger.tags
    assert [t.block for t in tags] == [1, 1, 2, 2]
    assert tags[0].pos == "DET:part"


def test83(tagger):
    tagger.tag("Degli studenti sono partiti")
    tags = tagger.tags
    assert [t.block for t in tags] == [1, 1, 2, 2]
    assert tags[0].pos == "DET:part"


def test84(tagger):
    tagger.tag("Sono partiti degli studenti")
    tags = tagger.tags
    assert [t.block for t in tags] == [1, 1, 2, 2]
    assert tags[2].pos == "DET:part"


@pytest.mark.skip
def test9(tagger):
    tagger.tag("Mi stupisco dei colleghi stranieri")
    tags = tagger.tags
    assert [t.block for t in tags] == [1, 1, 2, 2, 2]
    assert tags[-3].pos == "PRE:det"


def test10(tagger):
    tagger.tag("I cani si spaventano dei gatti")
    tags = tagger.tags
    assert [t.block for t in tags] == [1, 1, 2, 2, 3, 3]
    assert tags[-2].pos == "PRE:det"


def test11(tagger):
    tagger.tag("Lei è la più alta delle ragazze")
    tags = tagger.tags
    assert [t.block for t in tags] == [1, 2, 3, 3, 3, 3, 3]
    assert tags[-2].pos == "PRE:det"


@pytest.mark.skip
def test12(tagger):
    tagger.tag("Lui si appropria dei beni")
    tags = tagger.tags
    assert [t.block for t in tags] == [1, 2, 2, 3, 3]
    assert tags[-2].pos == "PRE:det"
    assert tags[0]._syntactic_role == "SOGG"


def test13(tagger):
    tagger.tag("Dei colleghi vennero chiamati")
    tags = tagger.tags
    assert [t.block for t in tags] == [1, 1, 2, 2]
    assert tags[0].pos == "DET:part"
    assert tags[0]._syntactic_role == "SOGG"
    assert tags[1]._syntactic_role == "SOGG"


def test14(tagger):
    tagger.tag("Vennero chiamati dei colleghi")
    tags = tagger.tags
    assert [t.block for t in tags] == [1, 1, 2, 2]
    assert tags[2].pos == "DET:part"
    assert tags[0].note == "AUX"
    assert tags[2]._syntactic_role == "SOGG"
    assert tags[3]._syntactic_role == "SOGG"


def test15(tagger):
    tagger.tag("Per me scorrere delle immagini è piacevole")
    tags = tagger.tags
    assert [t.block for t in tags] == [1, 1, 1, 1, 1, 2, 3]
    assert tags[3].pos == "DET:part"


def test16(tagger):
    tagger.tag("Per me lo scorrere delle immagini è piacevole")
    tags = tagger.tags
    assert [t.block for t in tags] == [1, 1, 2, 2, 2, 2, 3, 4]
    assert tags[4].pos == "PRE:det"


@pytest.mark.skip
def test17(tagger):
    tagger.tag("Quei tipi sono del professore")
    tags = tagger.tags
    assert [t.block for t in tags] == [1, 1, 2, 3, 3]
    assert tags[-2].pos == "PRE:det"


def test17_2(tagger):
    tagger.tag("Quei tipi erano del professore")
    tags = tagger.tags
    assert [t.block for t in tags] == [1, 1, 2, 3, 3]
    assert tags[-2].pos == "PRE:det"


@pytest.mark.skip
def test18(tagger):
    tagger.tag("Quei tipi sono dei professori")
    tags = tagger.tags
    assert [t.block for t in tags] == [1, 1, 2, 3, 3]
    assert tags[-2].pos == "DET:part|PRE:det"


def test18_2(tagger):
    tagger.tag("Quei tipi erano dei professori")
    tags = tagger.tags
    assert [t.block for t in tags] == [1, 1, 2, 3, 3]
    assert tags[-2].pos == "DET:part|PRE:det"


def test19(tagger):
    tagger.tag("Ci sono voluti dei professori")
    tags = tagger.tags
    assert [t.block for t in tags] == [1, 1, 1, 2, 2]
    assert tags[-2].pos == "DET:part"


def test20(tagger):
    tagger.tag("Dei colleghi ci sono voluti")
    tags = tagger.tags
    assert [t.block for t in tags] == [1, 1, 2, 2, 2]
    assert tags[0].pos == "DET:part"


def test21(tagger):
    tagger.tag("Dei colleghi si spaventano")
    tags = tagger.tags
    assert [t.block for t in tags] == [1, 1, 2, 2]
    assert tags[0].pos == "DET:part|PRE:det"


def test22(tagger):
    tagger.tag("Delle soluzioni ci sono state")
    tags = tagger.tags
    assert [t.block for t in tags] == [1, 1, 2, 2, 2]
    assert tags[0].pos == "DET:part"


def test23(tagger):
    tagger.tag("Delle sorelle è la più alta")
    tags = tagger.tags
    assert [t.block for t in tags] == [1, 1, 2, 3, 3, 3]
    assert tags[0].pos == "PRE:det"


def test24(tagger):
    tagger.tag("Delle amiche sono soddisfatte ")
    tags = tagger.tags
    assert [t.block for t in tags] == [1, 1, 2, 2]
    assert tags[0].pos == "DET:part|PRE:det"
