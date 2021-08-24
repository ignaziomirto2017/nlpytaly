from typing import List

from ....Tag import Tag

_data1 = [
    "bevve",
    "diede",
    "disse",
    "fece",
    "fu",
    "intervenne",
    "mosse",
    "nacque",
    "sopravvenne",
    "venne",
]

_data2 = [
    "bevvero",
    "diedero",
    "dissero",
    "fecero",
    "furono",
    "misero",
    "mossero",
    "nacquero",
    "vennero",
]


def pn_remo(tags: List[Tag]) -> None:
    """
    Person and number for "passato remoto"
    """
    for t in tags:
        if t.pos == "VER:remo":
            if t.occ in _data1:
                t.set_pn(3, "s")
            elif t.occ == "feci":
                t.set_pn(1, "s")
            elif t.occ in _data2:
                t.set_pn(3, "p")
            elif t.occ.endswith("i") and t.occ[-2] != "t":
                t.set_pn(1, "s")
            elif t.occ.endswith("sti"):
                t.set_pn(2, "s")
            elif t.occ.endswith("ò"):
                t.set_pn(3, "s")
            elif t.occ.endswith("ì"):
                t.set_pn(3, "s")
            elif t.occ.endswith("se"):
                t.set_pn(3, "s")
            elif t.occ.endswith("mmo"):
                t.set_pn(1, "p")
            elif t.occ.endswith("ste"):
                t.set_pn(2, "p")
            elif t.occ.endswith("rono"):
                t.set_pn(3, "p")
            elif t.occ.endswith("nnero"):
                t.set_pn(3, "p")
            elif t.occ.endswith("esero"):
                t.set_pn(3, "p")
            elif t.occ.endswith("insero"):
                t.set_pn(3, "p")
            elif t.occ.endswith("caddero"):
                t.set_pn(3, "p")
