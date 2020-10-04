from typing import List

from .gn_adj_poss import gn_poss_adj
from .gn_aggettivi import gn_aggettivi
from .gn_pp import gn_pp
from .gn_prep_art import gn_prep_art
from .gnp_articoli import gn_articoli, gn_sostantivi_successivi
from .nomi import nomi
from .pn_clitici import pn_clitici
from .pn_cond import pn_cond
from .pn_cong_imp import pn_congimp
from .pn_cong_pre import pn_congpre
from .pn_futu import pn_futu
from .pn_impe import pn_impe
from .pn_impf import pn_impf
from .pn_pres_ind import pn_pres_ind
from .pn_pro_demo import pn_pro_demo
from .pn_remo import pn_remo
from ...Tag import Tag


def features(tags: List[Tag]):
    pn_pro_demo(tags)
    gn_articoli(tags)
    gn_prep_art(tags)
    gn_aggettivi(tags)
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
    nomi(tags)
    gn_sostantivi_successivi(tags)
