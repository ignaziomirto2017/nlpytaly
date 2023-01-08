from typing import FrozenSet, Set

fs = frozenset

syns: Set[FrozenSet[str]] = {
    fs(("lestamente", "rapidamente", "velocemente")),
    fs(("cazzotto", "pugno")),
    fs(("lodare", "elogiare")),
    fs(("donare", "regalare")),
    fs(("con garbo", "garbatamente", "molto gentilmente")),
    fs(("foto", "fotografia")),
    fs(("balzare", "saltare")),
    fs(("balzo", "salto")),
    fs(("razzo", "missile")),
    fs(("schiaffo", "sberla", "sganassone", "ceffone", "scapaccione", "manrovescio")),
    fs(("schiaffi", "sberle", "sganassoni", "ceffoni", "scapaccioni", "manrovesci")),
    fs(("truppe", "milizie")),
}


def strip_articles(a: str, b: str):
    a = a.lower()
    b = b.lower()
    articles = {"il ", "lo ", "la ", "i ", "gli ", "le ", "un ", "un' ", "uno ", "una "}
    for art in articles:
        if art in a and art in b:
            a = a.replace(art, "")
            b = b.replace(art, "")
            return a, b
    return a, b


def are_synonyms(a: str, b: str):
    a, b = strip_articles(a, b)
    if a == b:
        return True
    for group in syns:
        if a in group and b in group:
            return True
    return False
