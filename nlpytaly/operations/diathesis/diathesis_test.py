from nlpytaly import NLPYTALY


def test1():
    nt = NLPYTALY()
    result = nt.tag("mi lavo")
    tags = result["tags"]
    assert tags[0].diathesis == "MIDDLE_PR"


def test2():
    nt = NLPYTALY()
    result = nt.tag("mi lavo. marco si lava. noi giochiamo. noi ce lo laviamo.")
    tags = result["tags"]
    assert tags[0].diathesis == "MIDDLE_PR"
    assert tags[4].diathesis == "MIDDLE_PR"
    assert tags[8].diathesis == "ACTIVE"
    assert tags[11].diathesis == "MIDDLE_PR"


def test3():
    nt = NLPYTALY()
    result = nt.tag("Lei è stata lavata.")
    tags = result["tags"]
    assert tags[1].diathesis == "PASSIVE"


def test4():
    nt = NLPYTALY()
    result = nt.tag("Oggi la politica è diventata un salotto di comunicazione")
    tags = result["tags"]
    assert tags[3].diathesis == "MIDDLE_MR"
    assert tags[4].diathesis == "MIDDLE_MR"


def test5():
    nt = NLPYTALY()
    result = nt.tag("Oggi la politica diventa un salotto di comunicazione")
    tags = result["tags"]
    assert tags[3].diathesis == "MIDDLE_MR"


def test6():
    nt = NLPYTALY()
    result = nt.tag("Quelle obiezioni furono fatte dalle donne al capo")
    tags = result["tags"]
    assert tags[3].diathesis == "PASSIVE"


def test7():
    nt = NLPYTALY()
    result = nt.tag("Ci sono delle persone")
    tags = result["tags"]
    assert tags[1].is_middle_mr()


def test8():
    nt = NLPYTALY()
    result = nt.tag("Ci sono state delle persone")
    tags = result["tags"]
    assert tags[1].is_middle_mr()
    assert tags[2].is_middle_mr()


def test9():
    nt = NLPYTALY()
    result = nt.tag("Ci sono tornate delle persone")
    tags = result["tags"]
    assert tags[1].is_middle_mr()
    assert tags[2].is_middle_mr()


def test10():
    nt = NLPYTALY()
    result = nt.tag("Si ride e si parte")
    tags = result["tags"]
    assert tags[0].is_middle_mr()
    assert tags[1].is_middle_mr()
    assert tags[3].is_middle_mr()
    assert tags[4].is_middle_mr()


def test11():
    nt = NLPYTALY()
    result = nt.tag("I professori si sono lavati")
    tags = result["tags"]
    assert tags[2].is_middle_pr()
    assert tags[3].is_middle_pr()
    assert tags[4].is_middle_pr()


def test12():
    nt = NLPYTALY()
    result = nt.tag("I bambini si sono addormentati")
    tags = result["tags"]
    assert tags[2].is_middle_mr()
    assert tags[3].is_middle_mr()
    assert tags[4].is_middle_mr()


def test13():
    nt = NLPYTALY()
    result = nt.tag("I bambini si addormentano")
    tags = result["tags"]
    assert tags[2].is_middle_mr()
    assert tags[3].is_middle_mr()
