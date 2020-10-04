import re
from typing import List

from ...Tag import Tag


def pn_pro_demo(tags: List[Tag]) -> None:
    quest_noun_regex = r"(quell')([a-z]+)"
    for t in tags:
        if t.lemma == "<unknown>":
            match = re.search(quest_noun_regex, t.occ)
            if match:
                prev_tags = tags[: t.index]
                new_tag = Tag(match.group(2), "NOM", "-")
                next_tags = tags[t.index + 1 :]
                t._occorrenza = re.search(quest_noun_regex, t.occ).group(1)
                t.pos = "PRO:demo"
                t.lemma = "quello"
                tags[:] = prev_tags + [t, new_tag] + next_tags
                for i, tag in enumerate(tags):
                    tag.index = i
    for t in tags:
        if t.pos == "PRO:demo":
            if t.occorrenza == "quest'" and t.lemma == "questo":
                t.set_pn(3, "s")
            elif t.occorrenza == "quell'" and t.lemma == "quello":
                t.set_pn(3, "s")
