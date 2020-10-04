from typing import List

from ...Tag import Tag
from ...data.verbi.meteo import verbi_meteo


def exclude_meteo_verbs(tags: List[Tag], indici_verbi_flessi):
    tmp = []
    for verbo in indici_verbi_flessi:
        tmp.append(
            any(
                tags[x].lemma in verbi_meteo for x in verbo if tags[x].is_verb()
            )  # escludo meteo verbs
        )
    for item in list(zip(indici_verbi_flessi, tmp)):
        i, remove_meteo_verb = item
        if remove_meteo_verb:
            indici_verbi_flessi.remove(i)
