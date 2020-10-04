from .meteo import verbi_meteo
from .verbi_classe_1 import verbi_classe_1
from .verbi_classe_2 import verbi_classe_2

all_intransitives = verbi_classe_1 | verbi_classe_2 | verbi_meteo
