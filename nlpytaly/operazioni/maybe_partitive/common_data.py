from ...data.agg_trigger_di import agg_trigger_di
from ...data.verbi.trigger_di import verb_trigger_di, verb_trigger_di_pron

determinanti = ["DET:def", "DET:indef", "PRO:demo", "PRO:indef"]

reggono_di = verb_trigger_di | verb_trigger_di_pron | agg_trigger_di
