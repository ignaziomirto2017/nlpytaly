from ...data.adj_trigger_di import adj_trigger_di_pp
from ...data.verbs.intransitives import all_intransitives
from .common_data import (
    adj_trigger_di,
    di_licenser,
    trigger_di_pron_verbs,
    trigger_di_verbs,
)


def process_next_block(
    next_block, tags, notes, blocks_done, t
):  # ANASTROFE: Pivot a SX
    if t.block in blocks_done or not next_block:
        return
    tmp = next_block[0]
    tags_next_2_blocks = t.get_next_block_tags(step=2)
    if tmp.any_occurrences_in_block(["ci", "c'"]):  # Delle soluzioni ci vogliono
        if tmp.is_lemma_in_block("volere") or all(
            x.lemma in ["essere", "stare"]
            for x in t.get_next_block_tags()
            if x.is_verb()
        ):
            t.pos = "DET:part"
            notes.append(
                f"{t.occurrence.upper()} is the partitive article of the topicalised subject"
            )
            blocks_done.add(t.block)
            return
    else:
        if t.block == 1 or next_block[0].any_lemmas_in_block(di_licenser):
            g = [x.number for x in t.get_next_block_tags() if x.is_inflected_verb()]
            h = [x.person for x in t.get_next_block_tags() if x.is_inflected_verb()]
            for p in tags_next_2_blocks:
                [x for x in t.get_next_block_tags() if x.is_inflected_verb()]
                if p.lemma in adj_trigger_di:
                    if (
                        "p" in g and "3rd" in h
                    ):  # Delle conseguenze/Dei professori sono consci ['noi' iniziale crea problemi]
                        notes.append(
                            f"Ambiguous phrase: {t.occurrence.upper()} is either a partitive article or\
                            a topicalized genitive licensed by {p.lemma.upper()}"
                        )
                        t.pos = "DET:part|PRE:det"
                        blocks_done.add(t.block)
                        return
                    else:  # Delle conseguenze/Dei professori siamo consci
                        notes.append(
                            f"{t.occurrence.upper()} is \
                            a topicalized genitive licensed by {p.lemma.upper()}"
                        )
                        blocks_done.add(t.block)
                        return
                # e.g. Dei risultati sono soddisfatte/Delle amiche sono soddisfatte
                if p.lemma in adj_trigger_di_pp:
                    notes.append(
                        f"Ambiguous phrase: {t.occurrence.upper()} is either a a partitive article or\
                        a topicalized genitive licensed by {p.lemma.upper()}"
                    )
                    t.pos = "DET:part|PRE:det"
                    blocks_done.add(t.block)
                    return
                if tags[t.index - 1].pos == "ADJ" and tags[t.index - 2].lemma in [
                    "meno",
                    "più",
                ]:
                    if tags[t.index - 3].lemma == "il":  # delle sorelle è la più alta
                        notes.append(
                            f"{t.occurrence.upper()} is part of a 'superlativo relativo'"
                        )
                        blocks_done.add(t.block)
                        return
            for p in t.get_next_block_tags():  # Dei risultati noi siamo soddisfatti
                if p.occurrence in adj_trigger_di_pp:
                    notes.append(
                        f"Ambiguous phrase: {t.occurrence.upper()} is either a a partitive article or\
                        a topicalized genitive licensed by {p.occurrence.upper()}"
                    )
                    t.pos = "DET:part|PRE:det"
                    blocks_done.add(t.block)
                    return
            for m in t.get_next_block_tags():
                if m.lemma in trigger_di_verbs | trigger_di_pron_verbs:
                    if t.match_pn(m):
                        if any(
                            x.lemma in ["di", "del"] for x in tags_next_2_blocks
                        ):  # Dei tipi parlano di noi/Delle ragazze si fidano di noi
                            notes.append(
                                f"{t.occurrence.upper()} (index {t.index}) is a partitive article"
                            )
                            t.pos = "DET:part"
                            blocks_done.add(t.block)
                            return
                        else:  # Dei tipi/Dei risultati parlano male; Delle ragazze si fidano
                            notes.append(
                                f"Ambiguous phrase: {t.occurrence.upper()} "
                                f"(index {t.index}) is either a topicalized genitive or a partitive article"
                            )
                            t.pos = "DET:part|PRE:det"
                            blocks_done.add(t.block)
                            return
                    else:  # e.g. Del ragazzo parlano
                        notes.append(
                            f"{t.occurrence.upper()} introduces a topicalized genitive licensed by {m.lemma.upper()}"
                        )
                        blocks_done.add(t.block)
                        return
                else:
                    if m.is_inflected_verb():
                        m_block = m.get_same_block_tags()
                        if t.match_pn(m):
                            if (
                                m_block[-1].lemma in all_intransitives
                                and m_block[-1].lemma
                                not in trigger_di_verbs | trigger_di_pron_verbs
                            ):
                                # e.g. Dei ragazzi intervengono
                                notes.append(
                                    f"{t.occurrence.upper()} is a partitive article\
                                    introducing the sentence subject"
                                )
                                t.pos = "DET:part"
                                blocks_done.add(t.block)
                                return
                        if m.is_passive() and t.match_pn(
                            m
                        ):  # Delle prove furono trovate dalla polizia
                            notes.append(
                                f"{t.occurrence.upper()} is a partitive article\
                                    introducing the sentence subject"
                            )
                            t.pos = "DET:part"
                            blocks_done.add(t.block)
                            return
                        elif m.is_middle_pr() and t.match_pn(
                            m
                        ):  # Delle prove si trovarono
                            notes.append(
                                f"{t.occurrence.upper()} is a partitive article\
                                    introducing the topicalised sentence subject"
                            )
                            t.pos = "DET:part"
                            blocks_done.add(t.block)
                            return
                        elif m.is_active():
                            if t.match_pn(m):  # Delle ragazze hanno visto
                                notes.append(
                                    f"{t.occurrence.upper()} is a partitive article"
                                )
                                t.pos = "DET:part"
                                blocks_done.add(t.block)
                                return
                            else:  # e.g. Dei ragazzi voglio; Dell'acqua voglio (e... Degli uomini diventeremo(?))
                                if m.lemma not in [
                                    "essere",
                                    "divenire",
                                    "diventare",
                                    "sembrare",
                                    "parere",
                                ]:
                                    notes.append(
                                        f"{t.occurrence.upper()} is a partitive article (topicalised)"
                                    )
                                    t.pos = "DET:part"
                                    blocks_done.add(t.block)
                                    return
