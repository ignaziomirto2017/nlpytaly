from typing import Dict

_syn = "synonym"
_pos = "pos"
_lemma = "multiword"


data: Dict[str, dict] = {
    "a": {
        "braccio": {"end": True, _syn: "improvvisando"},
        "casaccio": {"end": True, _syn: "a vanvera"},
        "cazzo": {"end": True, _syn: "a vanvera"},
        "intuito": {"end": True, _syn: "intuitivamente"},
        "lungo": {"end": True, _syn: "lungamente"},
        "meraviglia": {"end": True, _syn: "meravigliosamente"},
        "sufficienza": {"end": True, _syn: "sufficientemente"},
        "vanvera": {"end": True, _syn: "a casaccio"},
    },
    "al": {
        "contempo": {"end": True, _syn: "contemporaneamente"},
        # TODO:
        # Conflitto con mettere al corrente
        # "corrente": {
        #     "end": True,
        #     _syn: "sa",
        # },
    },
    "alla": {
        "follia": {"end": True, _syn: "follemente"},
        "lettera": {"end": True, _syn: "letteralmente"},
        "svelta": {"end": True, _syn: "rapidamente"},
        "perfezione": {"end": True, _syn: "perfettametne"},
    },
    "all'": {
        "improvviso": {"end": True, _syn: "improvvisamente"},
        "oscuro": {"end": True, _syn: "ignaro", _pos: "ADJ"},
    },
    "con": {
        "attenzione": {"end": True, _syn: "attentamente"},
        "cura": {"end": True, _syn: "accuratamente"},
    },
    "da": {
        "vigliacco": {"end": True, _syn: "vigliaccamente"},
        "codardo": {"end": True, _syn: "vigliaccamente"},
    },
    "di": {
        "botto": {"end": True, _syn: "improvvisamente"},
        "getto": {"end": True, _syn: "d'impulso"},
        "rilievo": {"end": True, _syn: "importante"},
        "punto": {"in": {"bianco": {"end": True, _syn: "improvvisamente"}}},
    },
    "due": {"passi": {"end": True, _syn: "passeggiata"}},
    "in": {
        "apparenza": {"end": True, _syn: "apparentemente"},
        "fretta": {"e": {"furia": {"end": True, _syn: "precipitosamente"}}},
        "sostanza": {"end": True, _syn: "sostanzialmente"},
        "tutto": {"end": True, _syn: "complessivamente"},
    },
}
