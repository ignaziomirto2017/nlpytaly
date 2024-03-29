from .common_data import inflected_verbs_pos


def is_verb(self) -> bool:
    return "VER:" in self.pos


def is_infinitive(self) -> bool:
    return ":infi" in self.pos


def is_npr(self) -> bool:
    return "NPR" in self.pos


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


def is_card(self) -> bool:
    return "@card@" in self.lemma


def is_past_participle(self) -> bool:
    return "VER:pper" in self.pos


def is_inflected_verb(self) -> bool:
    for v in inflected_verbs_pos:
        if v in self.pos:
            return True
    return False


def is_negative_inflected_verb(self) -> bool:
    if self._is_neg_sv is None:
        return False
    return True


def is_adverb(self) -> bool:
    return "ADV" in self.pos


def is_pro_pers(self) -> bool:
    return self.pos in ["PRO:pers", "PRO:pers:Sogg"]


def is_pro_poss(self) -> bool:
    return self.pos in ["PRO:poss"]


def is_pro_indef(self) -> bool:
    return self.pos in ["PRO:indef"]
