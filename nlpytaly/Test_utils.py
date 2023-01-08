import urllib.parse
from typing import Set

from nlpytaly import entailment

first_entails_second = -1
mutual_entailment = 0
no_entailment = None
second_entails_first = 1
in_common = 4


def get_ent_url(s1: str, s2: str):
    return f"http://localhost:3000/semroles/{urllib.parse.quote(s1 + '. ' + s2)}"


def entail_each_other(sentences: Set[str]):
    for s in sentences:
        for s_ in sentences:
            res, _, _, _ = entailment(s, s_)
            assert res == mutual_entailment, get_ent_url(s, s_)


# just_one used if sentence1 already tested with "entail_each_other"
def one_way_entailment(sentences1: Set[str], sentences2: Set[set], just_one=False):
    for g1 in sentences1:
        for g2 in sentences2:
            res, _, _, _ = entailment(g1, g2)
            assert res == first_entails_second, get_ent_url(g1, g2)
        if just_one:
            return
