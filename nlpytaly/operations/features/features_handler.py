from typing import List

from ._features.gn_adj_poss import gn_poss_adj
from ._features.gn_adjectives import gn_adjectives
from ._features.gn_pp import gn_pp
from ._features.gn_prep_art import gn_prep_art
from ._features.gnp_articles import (
    gn_articles,
    gn_following_nouns,
)
from ._features.nouns import nouns
from ._features.pn_clitics import pn_clitici
from ._features.pn_cond import pn_cond
from ._features.pn_cong_imp import pn_congimp
from ._features.pn_cong_pre import pn_congpre
from ._features.pn_futu import pn_futu
from ._features.pn_impe import pn_impe
from ._features.pn_impf import pn_impf
from ._features.pn_pres_ind import pn_pres_ind
from ._features.pn_pro_demo import pn_pro_demo
from ._features.pn_remo import pn_remo
from ...Tag import Tag


def features(tags: List[Tag]):
    pn_pro_demo(tags)
    gn_articles(tags)
    gn_prep_art(tags)
    gn_adjectives(tags)
    gn_pp(tags)
    gn_poss_adj(tags)
    pn_pres_ind(tags)
    pn_impf(tags)
    pn_futu(tags)
    pn_cond(tags)
    pn_remo(tags)
    pn_impe(tags)
    pn_congimp(tags)
    pn_congpre(tags)
    pn_clitici(tags)
    nouns(tags)
    gn_following_nouns(tags)
