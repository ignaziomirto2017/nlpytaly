from .common_data import *
from ...data.agg_trigger_di import agg_trigger_di_pp
from ...data.verbi.intransitives import all_intransitives
from ...operazioni.formazioni.formazione_infinito_riflessivo import (
    formazione_infinito_riflessivo,
)


# PIVOT A DX: UNMARKED WORD ORDER
def process_prev_block(prev_block, tags, notes, blocks_done, t):
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
        tmp.numero = "-"
        tmp.persona = "-"
        notes.append(f"{t.occorrenza.upper()} is the subject's partitive article")
        blocks_done.add(t.block)
        return
    elif all(
        x.lemma in ["essere", "stare"] for x in t.get_prev_block_tags() if x.is_verb()
    ):  # = frasi copulative
        if tmp.any_occurrences_in_block(["ci", "c'"]):
            t.pos = "DET:part"
            tmp.pos = "PRO:exist"
            tmp.numero = "—"
            tmp.persona = "—"
            notes.append(f"{t.occorrenza.upper()} is the subject's partitive article")
            blocks_done.add(t.block)
            return
        else:
            if (
                t.match_pn(tmp) and t.numero == "p"
            ):  # Quei tipi sono dei signori [± Animato] vs. 'la penna è del bambino
                notes.append(
                    f"The OF-phrase is ambiguous : {t.occorrenza.upper()} "
                    f"(index {t.index}) either introduces a genitive phrase or is a partitive article"
                )
                t.pos = "DET:part|PRE:det"
                blocks_done.add(t.block)
                return
            else:  # Quel libro è dei signori
                notes.append(
                    f"{t.occorrenza.upper()} (index {t.index}) introduces a genitive phrase"
                )
                blocks_done.add(t.block)
                return
    else:
        if prev_block[0].any_lemmas_in_block(reggono_di) or prev_block[
            0
        ].any_occurrences_in_block(agg_trigger_di_pp):
            for (
                p
            ) in (
                t.get_prev_block_tags()
            ):  # noi siamo soddisfatti dei risultati (TBTCO: Sono soddisfatte delle persone[ambiguo])
                if p.occorrenza in agg_trigger_di_pp:
                    notes.append(
                        f"{t.occorrenza.upper()} is a genitive licensed by {p.occorrenza.upper()}"
                    )
                    blocks_done.add(t.block)
                    return
                if p.lemma in verb_trigger_di:
                    if t.match_pn(p) and t.numero == "p":  # parlano dei ragazzi
                        notes.append(
                            f"Ambiguous phrase: {t.occorrenza.upper()}"
                            f"(index {t.index}) is either a genitive or a partitive article"
                        )
                        t.pos = "DET:part|PRE:det"
                        blocks_done.add(t.block)
                        return
                    else:  # Parliamo del ragazzo
                        notes.append(
                            f"{t.occorrenza.upper()} introduces a genitive phrase licensed by {p.lemma.upper()}"
                        )
                        blocks_done.add(t.block)
                        return
                if p.lemma in verb_trigger_di_pron:  # i cani (si) occupano dei gatti
                    if p.is_middle_pr():
                        notes.append(
                            f"{t.occorrenza.upper()} introduces a genitive phrase licensed by {formazione_infinito_riflessivo(p.lemma).upper()}"
                        )
                        blocks_done.add(t.block)
                        return
                    else:
                        notes.append(f"{t.occorrenza.upper()} is a partitive article")
                        t.pos = "DET:part"
                        blocks_done.add(t.block)
                        return
        elif prev_block[0].any_lemmas_in_block(
            all_intransitives
        ):  # Intervennero dei soldati
            for p in t.get_prev_block_tags():

                # rigo sotto: la seconda condizione per trattare 'Mi piace vedere delle immagini al computer'
                if (
                    p.lemma not in verb_trigger_di | verb_trigger_di_pron
                    and tags[t.index - 1].pos != "VER:infi"
                ):
                    notes.append(
                        f"{t.occorrenza.upper()} is a partitive article\
                            introducing the sentence subject"
                    )
                    t.pos = "DET:part"
                    blocks_done.add(t.block)
                    return
        else:
            for m in t.get_prev_block_tags():
                if m.is_inflected_verb():
                    if m.is_passive():  # Dalla polizia furono trovate delle prove
                        notes.append(
                            f"{t.occorrenza.upper()} is a partitive article\
                                introducing the sentence subject"
                        )
                        t.pos = "DET:part"
                        blocks_done.add(t.block)
                        return
                    elif m.is_middle_pr():  # 4 agosto 2020
                        if t.match_pn(m):  # si trovarono delle prove
                            notes.append(
                                f"{t.occorrenza.upper()} is a partitive article \
                                    introducing the sentence subject"
                            )
                        t.pos = "DET:part"
                        blocks_done.add(t.block)
                        return
                    elif m.is_active():
                        if t.match_pn(m):  # hanno visto delle ragazze
                            notes.append(
                                f"{t.occorrenza.upper()} is a partitive article"
                            )
                            t.pos = "DET:part"
                            blocks_done.add(t.block)
                            return
                        else:  # e.g. vogliamo dei ragazzi ; vorrei dell'acqua  (e... diventeremo degli uomini (?))
                            notes.append(
                                f"{t.occorrenza.upper()} is a partitive article"
                            )
                            t.pos = "DET:part"
                            blocks_done.add(t.block)
                            return
