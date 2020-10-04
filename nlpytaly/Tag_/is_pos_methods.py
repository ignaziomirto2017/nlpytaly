from .common_data import *


def is_verb(self) -> bool:
    return "VER:" in self.pos


def is_infinitive(self) -> bool:
    return ":infi" in self.pos


def is_gerund(self) -> bool:
    return ":geru" in self.pos


def is_article(self) -> bool:
    return "DET:" in self.pos


def is_noun(self) -> bool:
    return "NOM" in self.pos or "demo" in self.pos


def is_adjective(self) -> bool:
    return "ADJ" in self.pos


def is_preposition(self) -> bool:
    return "PRE" in self.pos


def is_past_participle(self) -> bool:
    return "VER:pper" in self.pos


def is_inflected_verb(self) -> bool:
    for v in verbi_flessi:
        if v in self.pos:
            return True
    return False


def is_adverb(self) -> bool:
    return "ADV" in self.pos


def is_pro_pers(self) -> bool:
    return self.pos in ["PRO:pers", "PRO:pers:Sogg"]
