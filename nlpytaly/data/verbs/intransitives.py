from .class_1_verbs import class_1_verbs
from .class_2_verbs import class_2_verbs
from .weather_verbs import weather_verbs

all_intransitives__no_weather = class_1_verbs | class_2_verbs
all_intransitives = all_intransitives__no_weather | weather_verbs
