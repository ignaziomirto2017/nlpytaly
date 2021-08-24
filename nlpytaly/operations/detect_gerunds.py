def detect_gerunds(tags):
    gerunds_tags = [x for x in tags if x.is_gerund()]
    for gerund in gerunds_tags:
        gerund.diathesis = "MIDDLE_PR" if gerund.occ.endswith("si") else "ACTIVE"
    return [
        [x.index]
        for x in gerunds_tags
        if tags[x.index - 1] and tags[x.index - 1].lemma != "stare"
    ]
