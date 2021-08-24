def reflexive_infinitive_formation(inf: str):
    """
    >>> reflexive_infinitive_formation('comporre')
    'comporsi'
    >>> reflexive_infinitive_formation('mangiare')
    'mangiarsi'
    """
    rules = [
        ("are", 1, "si"),
        ("ere", 1, "si"),
        ("ire", 1, "si"),
        ("rre", 2, "si"),
    ]
    for r in rules:
        if inf.endswith(r[0]):
            if r[1] == 0:
                return inf + "si"
            else:
                return inf[: -r[1]] + "si"
    return ""
