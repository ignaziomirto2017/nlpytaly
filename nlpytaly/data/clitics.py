from typing import Set

clitics: Set[str] = {
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

clitics_atm_2 = {"me", "te", "ce", "ve", "se"}

clitics_atm_1 = clitics - clitics_atm_2

reflexive_clitics: Set[str] = {
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

dir_obj_clitics: Set[str] = {"mi" "lo" "ci" "la" "l'" "le" "li" "ti" "vi"}
