from typing import Union

from ...Tag import Tag

# non funziona con e.g. 'merce', che finisce in 'e' ma è SG;
vowels = "aeiou"


def get_determinative(t: Tag):
    if isinstance(t, str):
        t = Tag(t, "VER", t)
    if t.is_npr():
        return Tag("", "DET:def", "")
    consonants = "bcdfglmnpqrstv"
    tmp = Tag("", "DET:def", "il")
    if t.number == "s":
        tmp.set_n("s")
        if t.occ[0] in vowels:
            tmp.occurrence = "l'"
            return tmp
        else:
            if t.gender == "m":
                t.set_g("m")
                if t.occ[0] == "s" and t.occ[1] in consonants:
                    tmp.occurrence = "lo"
                    return tmp
                tmp.occurrence = "il"
                return tmp
            tmp.set_g("f")
            tmp.occurrence = "la"
            return tmp
    else:
        tmp.set_n("p")
        if t.gender == "m":
            t.set_g("m")
            if t.occ[0] in vowels or (t.occ[0] == "s" and t.occ[1] in consonants):
                tmp.occurrence = "gli"
                return tmp
            tmp.occurrence = "i"
            return tmp
        tmp.set_g("f")
        tmp.occurrence = "le"
        return tmp


def get_determinative_inf(t: Union[Tag, str]):
    if isinstance(t, str):
        t = Tag(t, "VER", t)
    tmp = Tag("", "DET:def", "il")
    tmp.set_gn("m", "s")
    if t.occ[0] in vowels:
        tmp.occurrence = "l'"
    else:
        if t.occ[0] == "z":
            tmp.occurrence = "lo"
        elif t.occ[0] == "s" and t.occ[1] in "bcdfglmnpqtv":
            tmp.occurrence = "lo"
        else:
            tmp.occurrence = "il"
    return tmp
