_rules = [
    ("parte", 1, "ire"),
    ("stato", 2, "re"),
    ("stata", 2, "re"),
    ("stati", 2, "re"),
    ("state", 2, "re"),
    ("isto", 4, "edere"),
    ("isti", 4, "edere"),
    ("dato", 2, "re"),
    ("data", 2, "re"),
    ("dati", 2, "re"),
    ("date", 2, "re"),
    ("nto", 2, "gere"),
    ("nno", 3, "re"),
    ("ito", 2, "re"),
    ("ato", 2, "re"),
    ("ggi", 0, "are"),
    ("hi", 2, "are"),
    ("i", 1, "are"),
    ("e", 1, "ere"),
    ("o", 1, "are"),
    ("a", 1, "are"),
]


def infinitive_formation(o: str) -> str:  # o = occorrenza
    """
    >>> infinitive_formation("arrestato")
    'arrestare'
    >>> infinitive_formation("compianto")
    'compiangere'
    >>> infinitive_formation("amato")
    'amare'
    >>> infinitive_formation("mangiato")
    'mangiare'
    >>> infinitive_formation("visti")
    'vedere'
    >>> infinitive_formation("partito")
    'partire'
    >>> infinitive_formation("parte")
    'partire'
    """

    # rules = sorted(rules, reverse=True, key=lambda x: len(x[0]))
    for r in _rules:
        if o.endswith(r[0]):
            if r[1] == 0:
                return o + r[2]
            else:
                return o[: -r[1]] + r[2]
    return ""
