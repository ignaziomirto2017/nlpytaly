from typing import List

from ....Tag import Tag


def pn_pres_ind(tags: List[Tag]) -> None:
    """
    Person and number for "presente indicativo"
    """
    for t in tags:
        if "VER:pres" in t.pos:
            if t.occ in [
                "c'ha",
                "è",
                "é",
                "dà",
                "fa",
                "ha",
                "può",
                "sa",
                "sta",
                "va",
                "vive",
            ]:
                t.set_pn(3, "s")
            elif t.occ == "sono":
                t.set_pn(13, "s|p")
            elif t.occ == "suono":
                t.set_pn(1, "s")
            elif t.occ.endswith("i"):
                t.set_pn(2, "s")
            elif t.occ.endswith("iamo"):
                t.set_pn(1, "p")
            elif (
                len(t.occ) >= 4
                and t.occ[-4] != "i"
                and t.occ[-2] != "n"
                and t.occ.endswith("o")
            ):
                t.set_pn(1, "s")
            elif len(t.occ) >= 2 and t.occ.endswith("o") and t.occ[-2] != "n":
                t.set_pn(1, "s")
            elif t.occ == "ho" or t.occ.endswith("gno"):  # sogghigno
                t.set_pn(1, "s")
            elif t.occ.endswith("a"):
                t.set_pn(3, "s")
            elif (
                len(t.occ) >= 3
                and t.occ.endswith("e")
                and t.occ[-2] != "t"
                and t.occ[-3] != "t"
            ):
                t.set_pn(3, "s")
            elif (
                t.occ.endswith("ette")  # permette
                or t.occ.endswith("uol")  # vuol parlare
                or t.occ.endswith("atte")  # sbatte
                or t.occ.endswith("utre")  # nutre
            ):
                t.set_pn(3, "s")
            elif (
                t.occ.endswith("ente")  # sente
                or t.occ.endswith("erte")  # verte
                or t.occ.endswith("iste")  # consiste
            ):
                t.set_pn(3, "s")
            elif (
                len(t.occ) >= 3
                and t.occ.endswith("te")
                and t.occ[-3] not in ["n", "r", "s", "t"]
            ):
                t.set_pn(2, "p")
            elif (
                len(t.occ) >= 3 and t.occ.endswith("no") and t.occ[-3] not in ["i", "g"]
            ):
                t.set_pn(3, "p")
            elif t.occ in {"pettino"}:
                t.set_pn(1, "s")
