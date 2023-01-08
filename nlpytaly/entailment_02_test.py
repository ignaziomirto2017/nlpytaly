from nlpytaly import entailment
from nlpytaly.operations.semantic_roles.SemRole.consts import ACTV, ACTV_S, PASSV
from nlpytaly.operations.semantic_roles.SemRole.SemRole import (
    DativeSemRole,
    OrdinarySemRole,
)

from .operations.semantic_roles.utils import list_equals_no_order
from .Test_utils import (
    entail_each_other,
    entailment,
    first_entails_second,
    in_common,
    mutual_entailment,
    no_entailment,
    one_way_entailment,
    second_entails_first,
)


def test1():
    res, rs1, rs2, common = entailment(
        "Mario ha fatto regalare un orologio a me",
        "Mario mi ha fatto regalare un orologio",
    )
    assert res == mutual_entailment


def test2():
    res, rs1, rs2, common = entailment("Mario le manda", "Mario le manda i fiori")
    assert res == in_common
    expected_rs1 = [
        OrdinarySemRole("MARIO", ["MANDARE"], ACTV),
        OrdinarySemRole("3PF", ["MANDARE"], PASSV),
    ]
    list_equals_no_order(expected_rs1, rs1)
    expected_rs2 = [
        OrdinarySemRole("MARIO", ["MANDARE"], ACTV),
        DativeSemRole("3SF", ["MANDARE"]),
        OrdinarySemRole("I FIORI", ["MANDARE"], PASSV),
    ]
    list_equals_no_order(expected_rs2, rs2)
    expected_common = [
        OrdinarySemRole("MARIO", ["MANDARE"], ACTV),
    ]
    for ec in expected_common:
        assert ec in common["list"]
    assert len(common["list"]) == len(expected_common)


def test3():
    res, rs1, rs2, common = entailment(
        "Mario le ha suggerito le risposte", "Mario le ha suggerite"
    )
    assert res == in_common
    expected_rs1 = [
        OrdinarySemRole("MARIO", ["SUGGERIRE"], ACTV),
        DativeSemRole("3SF", ["SUGGERIRE"]),
        OrdinarySemRole("LE RISPOSTE", ["SUGGERIRE"], PASSV),
    ]
    list_equals_no_order(expected_rs1, rs1)
    expected_rs2 = [
        OrdinarySemRole("MARIO", ["SUGGERIRE"], ACTV),
        OrdinarySemRole("3PF", ["SUGGERIRE"], PASSV),
    ]
    list_equals_no_order(expected_rs2, rs2)
    expected_common = [
        OrdinarySemRole("MARIO", ["SUGGERIRE"], ACTV),
    ]
    for ec in expected_common:
        assert ec in common["list"]
    assert len(common["list"]) == len(expected_common)
