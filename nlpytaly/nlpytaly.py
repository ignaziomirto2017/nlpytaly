from typing import List

from .Tag import Tag
from .Utils import wording_syntactic_roles, save_sentence, get_diatheses
from .operazioni.blocchi_intermedi import get_blocchi_intermedi
from .operazioni.correzioni_occorrenza import correzioni_occorrenza
from .operazioni.crea_blocchi import crea_blocchi
from .operazioni.diatesi.diatesi_attiva_si_no import diatesi_attiva_mRFL
from .operazioni.diatesi.diatesi_passiva_si_no import diatesi_passiva_si_no
from .operazioni.diatesi.diatesi_riflessiva_si_no import diatesi_pRFL
from .operazioni.disambiguazione_nome_verb import disambigua_nome_verb
from .operazioni.disambiguazione_se_gli_la_le import disambiguazione_clitici
from .operazioni.fare_mestiere import trova_rs_mestieri_mark
from .operazioni.features.disambiguazione_sono import disambiguazione_sono
from .operazioni.features.features_handler import features
from .operazioni.locuzioni import locuzioni
from .operazioni.marcatore_luoghi import marca_luoghi
from .operazioni.maybe_partitive.maybe_partitive_controller import maybe_partitive
from .operazioni.preposizione_infinito import find_gerunds, trova_prep_piu_inf
from .operazioni.ricerca_candidati_sogg_ogg.handler import handler
from .operazioni.ruoli_sintattici.ruoli_sintattici import ruoli_sintattici
from .operazioni.trattamento_clitici_od import tratta_clitici
from .operazioni.trova_proclisi import trova_proclisi
from .operazioni.trova_verbo_flesso import trova_verbo_flesso
from .request_tags import request_tags


class nlpytaly(object):
    def __init__(self):
        self.tags: List[Tag] = []
        self.original_tags: List[Tag] = []
        self.sentence: str = ""

        self.ruoli_sintattici = {}
        self.notes: List[str] = []

        self._init = False

    def tag(self, sentence: str):
        self.get_tags(sentence)
        locuzioni(self.tags)
        correzioni_occorrenza(self.tags)
        disambigua_nome_verb(self.tags)
        features(self.tags)
        marca_luoghi(self.tags)

        tags_blocchi_tra_sintagmi_verbali = []
        proclisi, indici_proclisi = trova_proclisi(self.tags)
        verbi_flessi, indici_verbi_flessi = trova_verbo_flesso(
            self.tags, indici_proclisi
        )
        pi = trova_prep_piu_inf(self.tags)
        ger = find_gerunds(self.tags)
        indici_verbi_pp = sorted(indici_verbi_flessi + pi + ger, key=lambda x: x[0])
        if len(verbi_flessi) != 0:
            (
                blocchi_tra_sintagmi_verbali,
                tags_blocchi_tra_sintagmi_verbali,
                _,
            ) = get_blocchi_intermedi(self.tags, indici_verbi_pp)
            if len(blocchi_tra_sintagmi_verbali[0]) == 0:
                k = 2
            else:
                k = 1
            for blocco in blocchi_tra_sintagmi_verbali:
                if len(blocco) != 0:
                    for index in range(
                        min(blocco[0], len(self.tags) - 1),
                        min(blocco[-1] + 1, len(self.tags)),
                    ):
                        self.tags[index].block = k
                    k += 1
            crea_blocchi(self.tags, indici_verbi_pp)

        disambiguazione_sono(self.tags)
        disambiguazione_clitici(self.tags, indici_verbi_flessi)
        self.handle_diatesi(indici_proclisi, indici_verbi_flessi)
        maybe_partitive(self.tags, self.notes)
        pso_det = handler(tags_blocchi_tra_sintagmi_verbali, self.tags)
        rs_mestiere_indexes = trova_rs_mestieri_mark(self.tags)

        if len(verbi_flessi) != 0:
            indici_candidati = list()
            for item in pso_det:
                for tupla in item:
                    indici_candidati.append(tupla)
            ruoli_sintattici(
                sorted(indici_verbi_flessi),
                indici_candidati,
                self.tags,
                self.ruoli_sintattici,
                pi,
                ger,
                indici_proclisi,
                rs_mestiere_indexes,
            )
        tratta_clitici(self.tags, self.ruoli_sintattici)
        pi_occorrenze = []
        for index_block in pi:
            pi_occorrenze.append(
                " ".join([self.tags[x].occorrenza for x in index_block])
            )

        result = {
            "sentence": self.sentence,
            "tags": self.tags,
            "original_tags": self.original_tags,
            "diatheses": get_diatheses(self.tags),
            "Candidates for subjects and direct objects": pso_det,
            "Syntactic functions": wording_syntactic_roles(
                self.ruoli_sintattici, self.tags
            ),
            "Preposition plus infinitive": list(
                zip(pi_occorrenze, map(lambda x: f"{x}", pi))
            ),
            "Notes": self.notes,
        }
        return result

    def handle_diatesi(self, indici_proclisi, indici_verbi_flessi):
        diatesi_pRFL(self.tags, indici_verbi_flessi, indici_proclisi, self.notes)
        diatesi_passiva_si_no(self.tags, self.notes)
        diatesi_attiva_mRFL(self.tags)

    def get_tags(self, sentence: str):
        if self._init:
            self.__init__()
        self.sentence = sentence
        save_sentence(sentence)
        tags = request_tags(sentence)
        self.tags = [Tag(t[0], t[1], t[2]) for t in tags]
        self.original_tags = [t.copy() for t in self.tags]  # tags originali
        for i, t in enumerate(self.tags):
            self.tags[i].index = i
            self.tags[i].all_tags = self.tags
        self._init = True


if __name__ == "__main__":
    pass
