from nlpytaly import entailment

from .Test_utils import entailment, mutual_entailment, no_entailment


def test1():
    res, rs1, rs2, common = entailment(
        "Mario mangia la pasta",
        "Mario non mangia la pasta",
    )
    assert res is no_entailment


def test2():
    res, rs1, rs2, common = entailment(
        "Mario non mangia la pasta",
        "Mario non mangia la pasta",
    )
    assert res == mutual_entailment


def test3():
    res, rs1, rs2, common = entailment(
        "Mario mangia la pasta",
        "La pasta non è mangiata da Mario",
    )
    assert res is no_entailment


def test4():
    res, rs1, rs2, common = entailment(
        "Mario non mangia la pasta",
        "La pasta non è mangiata da Mario",
    )
    assert res == mutual_entailment


def test5():
    res, rs1, rs2, common = entailment(
        "Mario non mangia la pasta",
        "La pasta è mangiata",
    )
    assert res is no_entailment


def test6():
    res, rs1, rs2, common = entailment(
        "Mario prende a bacchettate l'amico", "L'amico non è bacchettato da Mario"
    )
    assert res is no_entailment


def test7():
    res, rs1, rs2, common = entailment(
        "Mario non prende a bacchettate l'amico", "L'amico non è bacchettato da Mario"
    )
    assert res == mutual_entailment


def test8():
    res, rs1, rs2, common = entailment(
        "Mario non prende a bacchettate l'amico", "L'amico non è bacchettato"
    )
    assert res is no_entailment
