from typing import List

from .utils import assign
from ...Tag import Tag
from ...data.verbs.class_2_verbs import class_2_verbs
from ...data.verbs.weather_verbs import weather_verbs


def passive(tags: List[Tag], notes: List[str]):
    blocks_done = set()
    for t in tags:
        sb_tags = t.get_same_block_tags()
        is_reflexive = t.is_middle()
        for p in sb_tags:
            if p.is_past_participle() and "stare" != p.lemma:
                pp = p
                break
        else:
            pp = None
        if t.lemma in ["venire", "essere"] and t.block not in blocks_done:
            blocks_done.add(t.block)
            if not is_reflexive and pp is not None:
                if pp.lemma in class_2_verbs:
                    notes.append(
                        f"Construction type: the verb phrase "
                        f"{' '.join([x.occurrence.upper() for x in sb_tags])} is intransitive."
                    )
                    break
                if pp.lemma in weather_verbs:
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
                        b_ = pp.number.upper()
                        b__ = pp.gender.upper()
                        notes.append(
                            f"The subject of the passive {' '.join([x.occurrence.upper() for x in sb_tags])}\
                                        has {t.person} person, '{b_}' number and  '{b__}' gender."
                        )
                        assign(tags, t, "PASSIVE")
                        for tnb in t.get_next_block_tags():
                            if tnb.lemma in ["da", "dal"]:
                                w = (
                                    f"{tnb.occurrence.upper()} "
                                    f"{tags[tnb.index + 1].occurrence.upper()} "
                                    f"is the by-phrase of a passive"
                                )
                                notes.append(w)
                                break
                        break
            elif is_reflexive and pp is not None:
                blocks_done.add(t.block)
