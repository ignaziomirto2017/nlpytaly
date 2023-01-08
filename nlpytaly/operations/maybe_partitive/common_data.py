from ...data.adj_trigger_di import adj_trigger_di
from ...data.verbs.trigger_di import trigger_di_pron_verbs, trigger_di_verbs

determiners = ["DET:def", "DET:indef", "PRO:demo", "PRO:indef"]

di_licenser = trigger_di_verbs | trigger_di_pron_verbs | adj_trigger_di
