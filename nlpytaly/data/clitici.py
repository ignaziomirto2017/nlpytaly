from typing import Set

clitici: Set[str] = {
    "mi",
    "ti",
    "si",
    "s'",
    "ci",
    "c'",
    "vi",
    "ne",
    "gli",
    "la",
    "lo",
    "li",
    "le",
    "l'",
    "se",
    "glielo",
    "gliela",
    "glieli",
    "gliele",
    "gliene",
    "non",
    "te",
    "ce",
    "me",
    "ve",
}

clitici_a_meno_due = {"me", "te", "ce", "ve", "se"}

clitici_a_meno_uno = clitici - clitici_a_meno_due

clitici_riflessivi: Set[str] = {
    "c'",
    "ci",
    "m'",
    "mi",
    "s'",
    "si",
    "t'",
    "ti",
    "v'",
    "vi",
}

clitici_od: Set[str] = {"mi" "lo" "ci" "la" "l'" "le" "li" "ti" "vi"}
