from typing import List

from nlpytaly.data.verbs.trivalent import trivalent_verbs

from ..data.ate_multiwords import ate_multiwords_colpire, ate_multiwords_insultare
from ..data.verbs.class_1_verbs import two_place_predicate1
from ..data.verbs.class_2_verbs import two_place_predicate2
from ..Tag import Tag
from ..Utils import get_attr
from .semantic_roles.pred_assigners import *


def OD_exists(syn_roles: dict, verb_indexes) -> bool:
    for _, value in syn_roles.items():
        role, verb_indexes_ = value
        if role == "OD" and verb_indexes == verb_indexes_:
            return True
    return False


def clitics_handler(tags: List[Tag], syn_roles: dict) -> None:
    # only for direct and indirect objects clitics
    for t in tags:
        if t.occ in ["mi", "ti", "ci", "vi", "gli", "le", "lo", "la"]:
            if t.is_in_SV_block():
                t.pos = "CLIT"
                verbs = [x for x in t.get_same_block_tags() if x.is_verb()]
                if verbs:
                    verb_tag = verbs[-1]
                    verb = verb_tag.lemma
                    if get_attr(verb_tag, pred_sem_fare_caus):
                        pass
                    elif get_attr(verb_tag, pred_syn_mest):
                        pass
                    elif get_attr(verb_tag, pred_syn_mettere_prep):
                        pass
                    elif data := get_attr(verb_tag, pred_syn_mettere_prep_ov):
                        pass
                    elif v := get_attr(verb_tag, pred_syn_ate):
                        if v in ate_multiwords_insultare:
                            verb = "insultare"
                        elif v in ate_multiwords_colpire:
                            verb = "colpire"
                    elif get_attr(t, pred_sem_pper):
                        pass
                    elif get_attr(t, pred_syn_supp):
                        pass

                    if (
                        verb
                        in two_place_predicate1 | two_place_predicate2 | trivalent_verbs
                    ):
                        match t.occ:
                            case "mi":
                                t.set_pn(1, "s")
                                t.note = "OGG INDIR"
                            case "ti":
                                t.set_pn(2, "s")
                                t.note = "OGG INDIR"
                            case "ci":
                                t.set_pn(1, "p")
                                t.note = "OGG INDIR"
                            case "vi":
                                t.set_pn(2, "p")
                                t.note = "OGG INDIR"
                            case "gli":
                                t.set_p(3)
                                t.note = "OGG INDIR"
                            case "la":
                                t.set_gn("f", "s")
                                t.set_p(3)
                                t.note = "OGG DIR"
                                syn_roles[(t.index,)] = (
                                    "OD",
                                    t.get_same_block_indexes(),
                                )
                            case "lo":
                                t.set_gn("m", "s")
                                t.set_p(3)
                                t.note = "OGG DIR"
                                syn_roles[(t.index,)] = (
                                    "OD",
                                    t.get_same_block_indexes(),
                                )
                            case "li":
                                t.set_gn("m", "p")
                                t.set_p(3)
                                t.note = "OGG DIR"
                                syn_roles[(t.index,)] = (
                                    "OD",
                                    t.get_same_block_indexes(),
                                )
                            case "le":
                                t.set_p(3)
                                t.set_g("f")
                                if verb in trivalent_verbs:
                                    if OD_exists(
                                        syn_roles, verb_tag.get_same_block_indexes()
                                    ):
                                        t.set_n("s")
                                        t.note = "OGG INDIR"
                                    else:
                                        t.set_n("p")
                                        t.note = "OGG DIR"
                                        syn_roles[(t.index,)] = (
                                            "OD",
                                            t.get_same_block_indexes(),
                                        )
                                else:
                                    if verb_tag.is_past_participle():
                                        if verb_tag.gender == "m":
                                            t.note = "OGG INDIR"
                                            t.set_n("s")
                                        else:
                                            t.note = "OGG DIR"
                                            syn_roles[(t.index,)] = (
                                                "OD",
                                                t.get_same_block_indexes(),
                                            )
                                    else:
                                        t.set_n("s")
                                        t.note = "OGG INDIR"

                    else:
                        match t.occ:
                            case "mi":
                                t.set_pn(1, "s")
                                t.note = "OGG DIR"
                                syn_roles[(t.index,)] = (
                                    "OD",
                                    t.get_same_block_indexes(),
                                )
                            case "ti":
                                t.set_pn(2, "s")
                                t.note = "OGG DIR"
                                syn_roles[(t.index,)] = (
                                    "OD",
                                    t.get_same_block_indexes(),
                                )
                            case "lo":
                                t.set_p(3)
                                t.set_gn("m", "s")
                                t.note = "OGG DIR"
                                syn_roles[(t.index,)] = (
                                    "OD",
                                    t.get_same_block_indexes(),
                                )
                            case "la":
                                t.set_p(3)
                                t.set_gn("f", "s")
                                t.note = "OGG DIR"
                                syn_roles[(t.index,)] = (
                                    "OD",
                                    t.get_same_block_indexes(),
                                )
                            case "gli":
                                t.set_p(3)
                                t.note = "OGG INDIR"
                            case "ci":
                                t.set_pn(1, "p")
                                t.note = "OGG DIR"
                                syn_roles[(t.index,)] = (
                                    "OD",
                                    t.get_same_block_indexes(),
                                )
                            case "vi":
                                t.set_pn(2, "p")
                                t.note = "OGG DIR"
                                syn_roles[(t.index,)] = (
                                    "OD",
                                    t.get_same_block_indexes(),
                                )
                            case "le":
                                t.set_p(3)
                                t.set_gn("f", "p")
                                t.note = "OGG DIR"
                                syn_roles[(t.index,)] = (
                                    "OD",
                                    t.get_same_block_indexes(),
                                )


def se_disambiguation(tags: List[Tag], indici_verbi_flessi: List[List[int]]):

    for group in indici_verbi_flessi:
        block: List[Tag] = tags[group[0]].get_same_block_tags()
        for tag in block:
            if tag.occ in ("se",):
                if tag.occurrence == "se":
                    tag.lemma = "si"
                tag.pos = "CLIT"


def clitics_disambiguation(
    tags: List[Tag], indici_verbi_flessi: List[List[int]], syn_roles: dict
):
    clitics_handler(tags, syn_roles)
    se_disambiguation(tags, indici_verbi_flessi)
