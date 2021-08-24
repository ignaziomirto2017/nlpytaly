from typing import List

from .exclude_weather_verbs import exclude_weather_verbs
from .left_side_search import nearest_candidate_left
from .right_side_search import nearest_candidate_right
from .utils import role_found
from ...Tag import Tag
from ...Utils import increment_blocks
from ...data.verbs.class_1_verbs import class_1_verbs


def syntactic_roles(
    indici_verbi_flessi: List[List[int]],
    indici_candidati: List[List[int]],
    tags: List[Tag],
    syn_role_dict,
    prep_inf: List[List[int]],
    gerunds: List[List[int]],
    indici_proclisi: List[List[int]],
    exclusions=None,
):
    subj_dict = {}

    exclude_weather_verbs(tags, indici_verbi_flessi)
    if exclusions is None:
        exclusions = []  # Lui fa >il meccanico<

    for step in [1, 2]:
        # sp = soggetto presunto
        results = nearest_candidate_left(
            indici_verbi_flessi,
            indici_proclisi,
            indici_candidati,
            tags,
            step,
            subj_dict,
        )
        for r in results:
            candidato_subj = r[0]
            verbo = r[1]
            v_indexes = tuple(tags[x] for x in verbo)
            v_indexes = v_indexes[0].get_same_block_indexes()  # per eventuali clitici
            sp__index = tuple(tags[x].index for x in candidato_subj)
            role_found(tags, sp__index, "SOGG", v_indexes, syn_role_dict)

        # op = oggetto presunto
        op = nearest_candidate_right(
            sorted(indici_verbi_flessi + prep_inf + gerunds, key=lambda x: x[0]),
            indici_candidati,
            tags,
            exclusions,
            step,
        )
        for o in op:
            op__indexes = tuple(tags[x].index for x in o[0])
            if (
                tuple(o[1]) in subj_dict and subj_dict[tuple(o[1])]
            ):  # verifica se è stato trovato il soggetto
                v_tags = [tags[x] for x in o[1]]
                if v_tags[
                    0
                ].is_passive():  # se il verbo è passivo, nessun OD da cercare
                    continue
                # distinguiamo tra PN e OD
                v = " ".join(x.lemma for x in v_tags if not x.is_aux() and x.is_verb())
                v_indexes = v_tags[0].get_same_block_indexes()
                if v in ["essere", "divenire", "diventare", "sembrare", "parere"]:
                    role_found(tags, op__indexes, "PN", v_indexes, syn_role_dict)
                else:
                    role_found(tags, op__indexes, "OD", v_indexes, syn_role_dict)
            else:  # se NON è stato trovato un SOGG per il verbo...
                o_tags = [tags[x] for x in o[0]]
                v_tags = [tags[x] for x in o[1]]
                v_indexes = tuple([v.index for v in v_tags])
                v_tag = [
                    t
                    for t in v_tags
                    if t.is_inflected_verb() or t.is_infinitive() or t.is_gerund()
                ][0]
                o_tag = [
                    t
                    for t in o_tags
                    if ("NOM" in t.pos or "NPR" in t.pos or "PRO:pers" in t.pos)
                ]
                if not o_tag:
                    continue
                else:
                    o_tag = o_tag[0]
                if v_tag.match_pn(o_tag):
                    if (
                        v_tags[0].is_passive()
                        or v_tags[0].is_middle()
                        or (
                            v_tags[0].is_active()
                            and any(v.lemma in class_1_verbs for v in v_tags)
                        )
                    ):
                        role_found(tags, op__indexes, "SOGG", v_indexes, syn_role_dict)
                    else:
                        role_found(
                            tags, op__indexes, "SOGG|OD", v_indexes, syn_role_dict
                        )
                else:
                    if v_tags[0].is_passive() or v_tags[0].is_middle_mr():
                        continue
                    role_found(tags, op__indexes, "OD", v_indexes, syn_role_dict)

    for key in syn_role_dict:
        start = key[0]
        end = key[-1]
        increment_blocks(tags, start, end)

    return syn_role_dict
