from typing import List

from .utils import assign
from ...Tag import Tag
from ...data.clitici import clitici_riflessivi
from ...data.verbi.verbi_classe_1 import verbi_classe_1
from ...data.verbi.verbi_classe_2 import verbi_classe_2


def diatesi_pRFL(
    tags: List[Tag],
    successione_indici_sv: List[List[int]],
    successione_indici_proclisi,
    notes: List[str],
):
    for i, indici_sv in enumerate(successione_indici_sv):
        proclisi_vs = successione_indici_proclisi[i]
        if len(proclisi_vs) != 0:
            if len(proclisi_vs) == 1:
                step = 1
                rightmost_index_proclisi = proclisi_vs[-step]
                tr = tags[rightmost_index_proclisi]
                tl = tags[tr.index + step]
                if tl.occorrenza == "sono" and tr.occorrenza == "ci":
                    assign(tags, tags[indici_sv[0]], "MIDDLE_MR")
                #
                elif (
                    tl.lemma in verbi_classe_1 | verbi_classe_2
                    and tl.persona == "3rd"
                    and tl.numero == "s"
                    and tr.lemma == "si"
                ):
                    notes.append("The sentence is impersonal")
                    tl.set_impersonal()
                    assign(tags, tags[indici_sv[0]], "MIDDLE_PR")
                elif tr.occorrenza in clitici_riflessivi and tr.match_pn(tl):
                    assign(tags, tags[indici_sv[0]], "MIDDLE_PR")
                else:
                    pass
            elif len(proclisi_vs) == 2:
                step = 2
                rightmost_index_proclisi = proclisi_vs[-step]
                tr = tags[rightmost_index_proclisi]
                tl = tags[tr.index + step]
                if tr.occorrenza in ["me", "te", "ce", "se", "ve"] and tr.match_pn(tl):
                    assign(tags, tags[indici_sv[0]], "MIDDLE_PR")
                if (
                    tags[tr.index + 1].occorrenza == "si"
                    and tl.persona == "3rd"
                    and tl.numero == "s"
                ):
                    notes.append("The sentence is impersonal")
                    tags[tr.index + 1].set_impersonal()
                    assign(tags, tags[indici_sv[0]], "MIDDLE_PR")
                elif tr.lemma == "non":
                    if tags[
                        rightmost_index_proclisi + 1
                    ].occorrenza in clitici_riflessivi and tags[
                        rightmost_index_proclisi + 1
                    ].match_pn(
                        tl
                    ):
                        assign(tags, tags[indici_sv[0]], "MIDDLE_PR")
                else:
                    pass
