from typing import List

from ...Tag import Tag


def disambiguazione_sono(tags: List[Tag]) -> None:
    for t in tags:
        if t.occorrenza == "sono":
            if t.index >= 1 and tags[t.index - 1].occorrenza == "si":
                t.set_pn(3, "p")
            elif t.index >= 1 and tags[t.index - 1].occorrenza == "mi":
                sb = t.get_same_block_tags()
                nb = t.get_next_block_tags()
                for tmp in sb:
                    if tmp.is_past_participle():
                        if tmp.is_plural():
                            t.set_pn(3, "p")
                            break
                        else:
                            t.set_pn(1, "s")
                            break
                else:
                    for tmp in nb:
                        if tmp.is_adjective() and tmp.is_plural():
                            t.set_pn(3, "p")
                            break
            else:
                ppers: List[Tag] = [
                    x for x in t.get_same_block_tags() if x.is_past_participle()
                ]
                if ppers:
                    pper = ppers[0]
                    if pper.is_plural():
                        t.set_pn(3, "p")
                    else:
                        t.set_pn(1, "s")
