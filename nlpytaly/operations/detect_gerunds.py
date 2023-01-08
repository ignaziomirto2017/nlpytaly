def detect_gerunds(tags):
    gerunds_tags = [x for x in tags if x.is_gerund()]
    for gerund in gerunds_tags:
        gerund.diathesis = "MIDDLE_PR" if gerund.occ.endswith("si") else "ACTIVE"

    return [
        [x.index]
        for x in gerunds_tags
        if not tags[x.index].prev()  # se il gerundio è a inizio frase
        # oppure
        or (
            (
                # non deve essere preceduto da stare (sta correndo)
                tags[x.index].prev().lemma != "stare"
                # o da avverbio (sta spesso correndo)
                and tags[x.index].prev().pos != "ADV"
            )
        )
    ]
