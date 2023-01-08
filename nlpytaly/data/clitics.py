from typing import Set

clitics_dir_obj: Set[str] = {
    "mi",
    "ti",
    "ci",
    "c'",
    "vi",
    "ne",
    "la",
    "lo",
    "li",
    "le",
    "l'",
}


clitics: Set[str] = {
    "si",
    "s'",
    "gli",
    "se",
    "gliel'",
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
} | clitics_dir_obj

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

dir_obj_clitics: Set[str] = {"mi", "lo", "ci", "la", "l'", "le", "li", "ti", "vi"}
