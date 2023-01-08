from .article_selection import get_determinative_inf


# verbs
def test1():
    for v in ["amare", "emergere", "odiare", "uscire"]:
        t = get_determinative_inf(v)
        assert t.occ == "l'"


def test2():
    for v in ["sbagliare", "spennare", "stremare", "studiare"]:
        t = get_determinative_inf(v)
        assert t.occ == "lo"


def test3():
    for v in ["camminare", "giocare", "mangiare", "parlare"]:
        t = get_determinative_inf(v)
        assert t.occ == "il"
