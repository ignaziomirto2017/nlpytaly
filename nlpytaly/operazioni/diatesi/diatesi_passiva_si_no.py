from typing import List

from .utils import assign
from ...Tag import Tag
from ...data.verbi.meteo import verbi_meteo
from ...data.verbi.verbi_classe_2 import verbi_classe_2


def diatesi_passiva_si_no(tags: List[Tag], notes: List[str]):
    blocks_done = set()
    for t in tags:
        sb_tags = t.get_same_block_tags()
        diatesi_riflessiva = t.is_middle_pr()
        for p in sb_tags:
            if p.is_past_participle() and "stare" != p.lemma:
                pp = p
                break
        else:
            pp = None
        if t.lemma in ["venire", "essere"] and t.block not in blocks_done:
            blocks_done.add(t.block)
            if not diatesi_riflessiva and pp is not None:
                if pp.lemma in verbi_classe_2:
                    notes.append(
                        f"Construction type: the sentence with "
                        f"{' '.join([x.occorrenza.upper() for x in sb_tags])} is intransitive."
                    )
                    break
                if pp.lemma in verbi_meteo:
                    notes.append(
                        f"The weather verb {pp.lemma.upper()} does not normally assign semantic roles"
                    )
                    break
                else:
                    if any(x.lemma in ["volere"] for x in sb_tags) and any(
                        x.lemma in ["ci", "c'"] for x in sb_tags
                    ):
                        pass
                    else:
                        b_ = pp.numero.upper()
                        b__ = pp.genere.upper()
                        notes.append(
                            f"The subject of the passive {' '.join([x.occorrenza.upper() for x in sb_tags])}\
                                        has {t.persona} person, '{b_}' number and  '{b__}' gender."
                        )
                        assign(tags, t, "PASSIVE")
                        for tnb in t.get_next_block_tags():
                            if tnb.lemma in ["da", "dal"]:
                                w = (
                                    f"{tnb.occorrenza.upper()} "
                                    f"{tags[tnb.index + 1].occorrenza.upper()} "
                                    f"is the by-phrase of a passive"
                                )
                                notes.append(w)
                                break
                        break
            elif diatesi_riflessiva and pp is not None:
                blocks_done.add(t.block)
