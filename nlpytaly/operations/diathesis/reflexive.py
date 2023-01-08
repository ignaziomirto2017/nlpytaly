from typing import List

from ...data.clitics import reflexive_clitics
from ...data.verbs.bivalent import v12_2si
from ...data.verbs.class_1_verbs import class_1_verbs
from ...data.verbs.class_2_verbs import class_2_verbs_, class_2_verbs_si
from ...Tag import Tag
from .utils import assign


def pRFL(
    tags: List[Tag],
    successione_indici_sv: List[List[int]],
    successione_indici_proclisi: List[List[int]],
    notes: List[str],
):
    for i, indici_sv in enumerate(successione_indici_sv):
        proclisi = successione_indici_proclisi[i]
        if tags[indici_sv[0 + len(proclisi)]].lemma in class_2_verbs_si:
            assign(tags, tags[indici_sv[0]], "MIDDLE_MR")
            continue
        if len(proclisi) == 1:
            step = 1
            last_proclisis_index = proclisi[-step]
            last_proclisis_tag = tags[last_proclisis_index]
            first_verb_tag = tags[last_proclisis_tag.index + step]
            last_verb_tag = [
                x for x in last_proclisis_tag.get_same_block_tags() if x.is_verb()
            ][-1]
            if (
                first_verb_tag.occurrence == "sono"
                and last_proclisis_tag.occurrence == "ci"
            ):
                assign(tags, tags[indici_sv[0]], "MIDDLE_MR")
            elif (
                last_verb_tag.lemma in class_1_verbs | class_2_verbs_
                and first_verb_tag.person == "3rd"
                and first_verb_tag.number == "s"
                and last_proclisis_tag.lemma == "si"
            ):
                notes.append("The sentence is impersonal")
                first_verb_tag.set_impersonal()
                assign(tags, tags[indici_sv[0]], "MIDDLE_MR")
            elif (
                last_proclisis_tag.occurrence in reflexive_clitics
                and last_proclisis_tag.match_pn(first_verb_tag)
            ):
                if last_verb_tag.lemma in v12_2si:
                    assign(tags, tags[indici_sv[0]], "MIDDLE_MR")
                else:
                    assign(tags, tags[indici_sv[0]], "MIDDLE_PR")
            else:
                pass
        elif len(proclisi) == 2:
            step = 2
            last_proclisis_index = proclisi[-step]
            last_proclisis_tag = tags[last_proclisis_index]
            first_verb_tag = tags[last_proclisis_tag.index + step]
            if (
                last_proclisis_tag.occurrence
                in [
                    "me",
                    "te",
                    "ce",
                    "se",
                    "ve",
                ]
                and last_proclisis_tag.match_pn(first_verb_tag)
            ):
                assign(tags, tags[indici_sv[0]], "MIDDLE_PR")
            if (
                tags[last_proclisis_tag.index + 1].occurrence == "si"
                and first_verb_tag.person == "3rd"
                and first_verb_tag.number == "s"
            ):
                notes.append("The sentence is impersonal")
                tags[last_proclisis_tag.index + 1].set_impersonal()
                assign(tags, tags[indici_sv[0]], "MIDDLE_PR")
            elif last_proclisis_tag.lemma == "non":
                if tags[
                    last_proclisis_index + 1
                ].occurrence in reflexive_clitics and tags[
                    last_proclisis_index + 1
                ].match_pn(
                    first_verb_tag
                ):
                    assign(tags, tags[indici_sv[0]], "MIDDLE_PR")
