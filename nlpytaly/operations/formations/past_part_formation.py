def past_part_formation(inf: str):
    """
    >>> past_part_formation("mangiare")
    'mangiato'
    >>> past_part_formation("assoggettare")
    'assoggettato'
    >>> past_part_formation("rateizzare")
    'rateizzato'
    >>> past_part_formation("partire")
    'partito'
    >>> past_part_formation("sedere")
    'seduto'
    >>> past_part_formation("restringere")
    'ristretto'
    >>> past_part_formation("fare")
    'fatto'
    >>> past_part_formation("fotografare")
    'fotografato'
    >>> past_part_formation("leggere")
    'letto'
    >>> past_part_formation("sconfiggere")
    'sconfitto'
    >>> past_part_formation("vedere")
    'veduto'
    >>> past_part_formation("nascere")
    'nato'
    >>> past_part_formation("bandire")
    'bandito'
    >>> past_part_formation("correre")
    'corso'
    >>> past_part_formation("redigere")
    'redatto'
    """
    inf = inf.lower()
    rules = [
        ("restringere", 10, "istretto"),
        ("infliggere", 5, "tto"),
        ("trafiggere", 5, "tto"),
        ("stringere", 6, "etto"),
        ("prevedere", 5, "isto"),
        ("prendere", 5, "so"),
        ("nfiggere", 5, "tto"),
        ("redigere", 5, "atto"),
        ("mpere", 5, "tto"),
        ("gnere", 5, "nto"),
        ("assumere", 4, "nto"),
        ("radere", 4, "so"),
        ("scorrere", 4, "so"),
        ("scoperta", 4, "erto"),
        ("inferire", 3, "to"),
        ("astidire", 2, "to"),
        ("cuotere", 6, "osso"),
        ("rendere", 5, "so"),
        ("figgere", 5, "sso"),
        ("nascere", 5, "to"),
        ("correre", 4, "so"),
        ("ncedere", 4, "sso"),
        ("corgere", 4, "to"),
        ("vendere", 3, "uto"),
        ("battere", 3, "uto"),
        ("bandire", 2, "to"),
        ("inorridire", 2, "to"),
        ("grafare", 2, "to"),
        ("gredire", 2, "to"),
        ("uovere", 6, "osso"),
        ("ondere", 6, "uso"),
        ("ellere", 6, "ulso"),
        ("gliere", 6, "lto"),
        ("endere", 5, "so"),
        ("veder", 5, "isto"),
        ("ondere", 5, "sto"),
        ("olvere", 4, "to"),
        ("iedere", 4, "sto"),
        ("vivere", 4, "ssuto"),
        ("scrivere", 4, "tto"),
        ("prescrivere", 4, "tto"),
        ("parere", 3, "so"),
        ("endere", 3, "uto"),
        ("venire", 3, "uto"),
        ("audire", 2, "to"),
        ("ttere", 5, "sso"),
        ("igere", 5, "etto"),
        ("valere", 3, "so"),
        ("ncere", 4, "to"),
        ("utere", 4, "sso"),
        ("rgere", 4, "so"),
        ("prire", 4, "erto"),
        ("scere", 3, "iuto"),
        ("edere", 3, "uto"),
        ("adere", 3, "uto"),
        ("dere", 4, "so"),
        ("ggere", 5, "tto"),
        ("gere", 4, "to"),
        ("urre", 4, "otto"),
        ("cere", 3, "iuto"),
        ("bere", 3, "evuto"),
        ("arre", 3, "tto"),
        ("orre", 3, "sto"),
        ("dire", 3, "etto"),
        ("fare", 4, "fatto"),
        ("ere", 3, "uto"),
        ("are", 2, "to"),
        ("ire", 2, "to"),
    ]
    # rules = sorted(rules, reverse=True, key=lambda x: (len(x[0]), x[1]))
    # print(rules)
    for r in rules:
        if inf.endswith(r[0]):
            if r[1] == 0:
                return inf + r[2]
            else:
                return inf[: -r[1]] + r[2]
    return ""


if __name__ == "__main__":
    past_part_formation("giocare")
