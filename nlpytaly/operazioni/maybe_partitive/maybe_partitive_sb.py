from .common_data import *


def process_same_block(t_block, tags, notes, blocks_done, t):
    # Trattamento di un eventuale infinito prima del pivot
    infi_esiste = any(
        [
            x
            for x in t.get_same_block_tags()
            if x.pos == "VER:infi" and x.index < t.index
        ]
    )
    infi_index = [
        x.index
        for x in t.get_same_block_tags()
        if x.pos == "VER:infi" and x.index < t.index
    ]  # è l'indice dell'infinito
    if infi_esiste:
        det_esiste = any(
            [
                x
                for x in t.get_same_block_tags()
                if x.pos in determinanti and x.index < infi_index[0]
            ]
        )  # il det precede l'infinito
        if det_esiste:  # Per me il continuo scorrere delle immagini è piacevole
            notes.append(
                f"{t.occorrenza.upper()} (index {t.index}) introduces a genitive phrase"
            )
            blocks_done.add(t.block)
            return
        else:  # Per me scorrere delle immagini è piacevole
            notes.append(
                f"{t.occorrenza.upper()} (index {t.index}) introduces a partitive"
            )
            t.pos = "DET:part"
            blocks_done.add(t.block)
            return
    # COMPLEMENTI RETTI DA NOMI, 'PRIMA', SUPERLATIVI, COMPARATIVI, AGGETTIVI (tutto dentro il MEDESIMO blocco)
    for x in t_block:
        if (
            x.index > 0 and t.index - x.index >= 1
        ):  # prima del pivot ci sono almeno due occorrenze
            if (
                tags[t.index - 1].pos in ["NOM", "NPR"]
                or tags[t.index - 2].pos == "NOM"
            ):
                notes.append(
                    f"{t.occorrenza.upper()} (index {t.index}) introduces a genitive phrase"
                )
                blocks_done.add(t.block)
                return
        if tags[t.index - 1].occorrenza == "prima":
            notes.append(
                f"{t.occorrenza.upper()} (index {t.index}) introduces a genitive phrase"
            )
            blocks_done.add(t.block)
            return
        if tags[t.index - 1].pos == "ADJ" and tags[t.index - 2].lemma in [
            "meno",
            "più",
        ]:
            if tags[t.index - 3].lemma == "il":  # è la più alta delle sorelle
                notes.append(
                    f"{t.occorrenza.upper()} is part of a 'superlativo relativo'"
                )
            else:
                notes.append(
                    f"{t.occorrenza.upper()} introduces the second member of a comparative"
                )
            blocks_done.add(t.block)
            return
        if x.lemma in agg_trigger_di:  # Lea è conscia delle difficoltà
            notes.append(
                f"{t.occorrenza.upper()} introduces a genitive licensed by the adjective {x.lemma.upper()}"
            )
            blocks_done.add(t.block)
            return
