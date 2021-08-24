from typing import Dict

data: Dict[str, dict] = {
    "a": {
        "braccio": {"end": True, "sinonimo": "improvvisando",},
        "cazzo": {"end": True, "sinonimo": "a vanvera",},
        "intuito": {"end": True, "sinonimo": "intuitivamente",},
        "lungo": {"end": True, "sinonimo": "lungamente",},
        "meraviglia": {"end": True, "sinonimo": "meravigliosamente",},
        "sufficienza": {"end": True, "sinonimo": "sufficientemente",},
        "vanvera": {"end": True, "sinonimo": "troppo",},
    },
    "al": {"contempo": {"end": True, "sinonimo": "contemporaneamente",},},
    "alla": {
        "follia": {"end": True, "sinonimo": "follemente",},
        "lettera": {"end": True, "sinonimo": "letteralmente",},
        "svelta": {"end": True, "sinonimo": "sveltamente",},
        "perfezione": {"end": True, "sinonimo": "perfettametne",},
    },
    "all'": {
        "improvviso": {"end": True, "sinonimo": "improvvisamente",},
        "oscuro": {"end": True, "sinonimo": "ignaro", "pos": "ADJ"},
    },
    "di": {
        "botto": {"end": True, "sinonimo": "improvvisamente",},
        "getto": {"end": True, "sinonimo": "d'impulso",},
        "rilievo": {"end": True, "sinonimo": "molto importante",},
        "punto": {"in": {"bianco": {"end": True, "sinonimo": "improvvisamente"}}},
    },
    "in": {
        "apparenza": {"end": True, "sinonimo": "apparentemente",},
        "sostanza": {"end": True, "sinonimo": "sostanzialmente",},
        "tutto": {"end": True, "sinonimo": "complessivamente",},
    },
}
