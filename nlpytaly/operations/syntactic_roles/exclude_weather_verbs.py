from typing import List

from ...Tag import Tag
from ...data.verbs.weather_verbs import weather_verbs


def exclude_weather_verbs(tags: List[Tag], indici_verbi_flessi):
    # No subject or direct object search
    tmp = []
    for verb in indici_verbi_flessi:
        tmp.append(
            any(tags[x].lemma in weather_verbs for x in verb if tags[x].is_verb())
        )
    for item in list(zip(indici_verbi_flessi, tmp)):
        i, remove_meteo_verb = item
        if remove_meteo_verb:
            indici_verbi_flessi.remove(i)
