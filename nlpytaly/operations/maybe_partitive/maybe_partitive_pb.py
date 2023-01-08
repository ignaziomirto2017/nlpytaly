from typing import List

from ...data.adj_trigger_di import adj_trigger_di_pp
from ...data.verbs.intransitives import all_intransitives
from ...operations.formations.reflexive_infinitive_formation import (
    reflexive_infinitive_formation,
)
from ...Tag import Tag
from .common_data import di_licenser, trigger_di_pron_verbs, trigger_di_verbs


# PIVOT A DX: UNMARKED WORD ORDER
def process_prev_block(prev_block: List[Tag], tags, notes, blocks_done, t):
    if t.block in blocks_done:
        return
    if not prev_block:
        return
    tmp = prev_block[0]
    # Ci vogliono delle cose / Ci sono (state) delle cose
    if tmp.any_occurrences_in_block(["ci", "c'"]) and tmp.is_lemma_in_block(
        "volere"
    ):  # e.g. ci vuole del gelato
        t.pos = "DET:part"
        tmp.pos = "PRO:exist"
        tmp.number = "-"
        tmp.person = "-"
        notes.append(f"{t.occurrence.upper()} is the subject's partitive article")
        blocks_done.add(t.block)
        return
    elif all(
        x.lemma in ["essere", "stare"] for x in t.get_prev_block_tags() if x.is_verb()
    ):  # = frasi copulative
        if tmp.any_occurrences_in_block(["ci", "c'"]):
            t.pos = "DET:part"
            tmp.pos = "PRO:exist"
            tmp.number = "—"
            tmp.person = "—"
            notes.append(f"{t.occurrence.upper()} is the subject's partitive article")
            blocks_done.add(t.block)
            return
        else:
            if (
                t.match_pn(tmp) and t.number == "p"
            ):  # Quei tipi sono dei signori [± Animato] vs. 'la penna è del bambino
                notes.append(
                    f"The OF-phrase is ambiguous : {t.occurrence.upper()} "
                    f"(index {t.index}) either introduces a genitive phrase or is a partitive article"
                )
                t.pos = "DET:part|PRE:det"
                blocks_done.add(t.block)
                return
            else:  # Quel libro è dei signori
                notes.append(
                    f"{t.occurrence.upper()} (index {t.index}) introduces a genitive phrase"
                )
                blocks_done.add(t.block)
                return
    else:
        if prev_block[0].any_lemmas_in_block(di_licenser) or prev_block[
            0
        ].any_occurrences_in_block(adj_trigger_di_pp):
            for (
                p
            ) in (
                t.get_prev_block_tags()
            ):  # noi siamo soddisfatti dei risultati (compare to Sono soddisfatte delle persone[ambiguo])
                if p.occurrence in adj_trigger_di_pp:
                    notes.append(
                        f"{t.occurrence.upper()} is a genitive licensed by {p.occurrence.upper()}"
                    )
                    blocks_done.add(t.block)
                    return
                if p.lemma in trigger_di_verbs:
                    if t.match_pn(p) and t.number == "p":  # parlano dei ragazzi
                        notes.append(
                            f"Ambiguous phrase: {t.occurrence.upper()}"
                            f"(index {t.index}) is either a genitive or a partitive article"
                        )
                        t.pos = "DET:part|PRE:det"
                        blocks_done.add(t.block)
                        return
                    else:  # Parliamo del ragazzo
                        notes.append(
                            f"{t.occurrence.upper()} introduces a genitive phrase licensed by {p.lemma.upper()}"
                        )
                        blocks_done.add(t.block)
                        return
                if p.lemma in trigger_di_pron_verbs:  # i cani (si) occupano dei gatti
                    if p.is_middle_mr():
                        notes.append(
                            f"{t.occurrence.upper()} introduces a genitive phrase licensed by {reflexive_infinitive_formation(p.lemma).upper()}"
                        )
                        blocks_done.add(t.block)
                        return
                    else:
                        notes.append(f"{t.occurrence.upper()} is a partitive article")
                        t.pos = "DET:part"
                        blocks_done.add(t.block)
                        return
        elif prev_block[0].any_lemmas_in_block(
            all_intransitives
        ):  # Intervennero dei soldati
            for p in t.get_prev_block_tags():

                # rigo sotto: la seconda condizione per trattare 'Mi piace vedere delle immagini al computer'
                if (
                    p.lemma not in trigger_di_verbs | trigger_di_pron_verbs
                    and tags[t.index - 1].pos != "VER:infi"
                ):
                    notes.append(
                        f"{t.occurrence.upper()} is a partitive article\
                            introducing the sentence subject"
                    )
                    t.pos = "DET:part"
                    blocks_done.add(t.block)
                    return
        else:
            for m in t.get_prev_block_tags():
                m: Tag
                if m.is_inflected_verb() or m.is_infinitive() or m.is_gerund:
                    if m.is_passive():  # Dalla polizia furono trovate delle prove
                        notes.append(
                            f"{t.occurrence.upper()} is a partitive article\
                                introducing the sentence subject"
                        )
                        t.pos = "DET:part"
                        blocks_done.add(t.block)
                        return
                    elif m.is_middle_pr():
                        if t.match_pn(m):  # si trovarono delle prove
                            notes.append(
                                f"{t.occurrence.upper()} is a partitive article \
                                    introducing the sentence subject"
                            )
                        t.pos = "DET:part"
                        blocks_done.add(t.block)
                        return
                    elif m.is_active():
                        if t.match_pn(m):  # hanno visto delle ragazze
                            notes.append(
                                f"{t.occurrence.upper()} is a partitive article"
                            )
                            t.pos = "DET:part"
                            blocks_done.add(t.block)
                            return
                        else:  # e.g. vogliamo dei ragazzi ; vorrei dell'acqua  (e... diventeremo degli uomini (?))
                            notes.append(
                                f"{t.occurrence.upper()} is a partitive article"
                            )
                            t.pos = "DET:part"
                            blocks_done.add(t.block)
                            return
