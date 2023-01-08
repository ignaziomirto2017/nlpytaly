from typing import List

from ....data.gn_determiners import gn_determiners as dict_
from ....Tag import Tag


def gn_articles(tags: List[Tag]) -> None:
    """
    Gender and number for articles
    """
    for t in tags:
        if t.occurrence in dict_:
            g, n = dict_[t.occurrence].split("+")
            t.set_gn(g, n)
            t.set_p(3)


def gn_following_nouns(tags: List[Tag]):
    """
    Gender and number for following nouns

    una danza
    una: f. s. => danza f. s.

    mio nipote
    mio: m. s. => nipote m. s.
    mia nipote
    mia: f. s. => nipote f. s.
    """
    for i, t in enumerate(tags):
        if (
            t.is_article()
            or ":det" in t.pos
            or "PRO:demo" in t.pos
            or t.is_pro_poss()
            or t.pos == "PRO:indef"
        ):
            if i + 1 < len(tags) and tags[i + 1].pos == "NOM":
                tags[i + 1].set_gn(t.gender, t.number)
