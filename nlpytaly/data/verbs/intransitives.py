from .class_1_verbs import class_1_verbs, two_place_predicate1
from .class_2_verbs import class_2_verbs
from .weather_verbs import weather_verbs

all_intransitives__no_weather = class_1_verbs | class_2_verbs | two_place_predicate1
all_intransitives = all_intransitives__no_weather | weather_verbs
