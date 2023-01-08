from typing import List

from ...Tag import Tag


def sono_disambiguation(tags: List[Tag]) -> None:
    """
    "Sono" person disambiguation (1st s or 3rd p).
    """
    for t in tags:
        if t.occ == "sono":
            prev = t.prev()
            next = t.next()

            # Si sono ...
            if prev and prev.occ == "si":
                t.set_pn(3, "p")

            # Mi sono ...
            elif prev and prev.occ == "mi":
                sb = t.get_same_block_tags()
                nb = t.get_next_block_tags()
                for tmp in sb:
                    if tmp.is_past_participle():
                        # ... concessi
                        if tmp.is_plural():
                            t.set_pn(3, "p")
                            break
                        # ... concesso
                        else:
                            t.set_pn(1, "s")
                            break
                else:
                    for tmp in nb:
                        if tmp.is_adjective():
                            # ... antipatici
                            if tmp.is_plural():
                                t.set_pn(3, "p")
                                break
                            # ... antipatico
                            elif tmp.is_singular():
                                t.set_pn(3, "s")
                                break

            # ... antipatic*
            elif next and next.is_adjective():
                if next.is_singular():
                    t.set_pn(1, "s")
                elif next.is_plural():
                    t.set_pn(3, "p")
            else:
                ppers: List[Tag] = [
                    x for x in t.get_same_block_tags() if x.is_past_participle()
                ]
                if ppers:
                    pper = ppers[0]
                    # ... criticat*
                    if pper.is_plural():
                        t.set_pn(3, "p")
                    else:
                        t.set_pn(1, "s")
