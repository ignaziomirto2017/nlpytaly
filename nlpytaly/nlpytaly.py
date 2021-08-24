from typing import List, Tuple

from .Tag import Tag
from .Utils import wording_syntactic_roles, save_sentence, get_diatheses
from .data.verbs.class_2_verbs import class_2_verbs
from .operations.clitics_as_direct_objs import clitics_as_dir_objs
from .operations.clitics_disambiguation import clitics_disambiguation
from .operations.corrections_by_occurrence import occurence_corrections
from .operations.create_blocks import create_blocks
from .operations.detect_gerunds import detect_gerunds
from .operations.detect_inflected_verbs.detect_inflected_verbs import (
    detect_inflected_verbs,
)
from .operations.detect_proclisis.detect_proclisis import detect_proclisis
from .operations.diathesis.active import active_mRFL
from .operations.diathesis.passive import passive
from .operations.diathesis.reflexive import pRFL
from .operations.diathesis.utils import assign
from .operations.features.features_handler import features
from .operations.features.sono_disambiguation import sono_disambiguation
from .operations.intermediate_blocks import get_intermediate_blocks
from .operations.maybe_partitive.maybe_partitive_controller import maybe_partitive
from .operations.multiwords import multiwords
from .operations.noun_verb_disambiguation import noun_verb_disambiguation
from .operations.place_marker import place_marker
from .operations.preposition_plus_infinitive import detect_prep_plus_infinitive
from .operations.search_sub_obj_candidates.handler import candidates_handler
from .operations.semantic_roles.PredFinder import mark
from .operations.semantic_roles.PredFinder import pred_finder
from .operations.semantic_roles.SemRole import AbstractSemRole
from .operations.semantic_roles.causative_fare_construction import mark_causative_fare
from .operations.semantic_roles.job_fare_construction import mark_job_sem_role
from .operations.syntactic_roles.syntactic_roles import syntactic_roles
from .request_tags import request_tags


class NLPYTALY(object):
    def __init__(self):
        self._init = False

        self.tags: List[Tag] = []
        self.original_tags: List[Tag] = []

        self.sentence: str = ""

        self.syntactic_roles = {}
        self.semantic_roles: List[AbstractSemRole] = []

        self.notes: List[str] = []

        self.sem_roles_cov_subjects = {}

    def tag(self, sentence: str):
        self.get_tags(sentence)
        multiwords(self.tags)
        occurence_corrections(self.tags)
        noun_verb_disambiguation(self.tags)
        features(self.tags)
        place_marker(self.tags)

        tags_blocchi_tra_sintagmi_verbali = []
        proclisis, proclisis_indexes = detect_proclisis(self.tags)
        inflected_verbs, inflected_verbs_indexes = detect_inflected_verbs(
            self.tags, proclisis_indexes
        )
        prep_plus_infinitive = detect_prep_plus_infinitive(self.tags)
        gerunds = detect_gerunds(self.tags)
        indici_verbi_pp = sorted(
            inflected_verbs_indexes + prep_plus_infinitive + gerunds, key=lambda x: x[0]
        )
        if len(inflected_verbs) != 0:
            (
                blocchi_tra_sintagmi_verbali,
                tags_blocchi_tra_sintagmi_verbali,
                _,
            ) = get_intermediate_blocks(self.tags, indici_verbi_pp)
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
            create_blocks(self.tags, indici_verbi_pp)

        sono_disambiguation(self.tags)
        clitics_disambiguation(self.tags, inflected_verbs_indexes)
        self.handle_diathesis(proclisis_indexes, inflected_verbs_indexes)
        maybe_partitive(self.tags, self.notes)
        potential_sub_obj = candidates_handler(
            tags_blocchi_tra_sintagmi_verbali, self.tags
        )
        direct_obj_exclusions = mark_job_sem_role(self.tags)

        if len(inflected_verbs) != 0:
            indici_candidati = list()
            for item in potential_sub_obj:
                for tupla in item:
                    indici_candidati.append(tupla)
            syntactic_roles(
                sorted(inflected_verbs_indexes),
                indici_candidati,
                self.tags,
                self.syntactic_roles,
                prep_plus_infinitive,
                gerunds,
                proclisis_indexes,
                direct_obj_exclusions,
            )
        clitics_as_dir_objs(self.tags, self.syntactic_roles)
        pi_occorrenze = []
        for index_block in prep_plus_infinitive:
            pi_occorrenze.append(
                " ".join([self.tags[x].occurrence for x in index_block])
            )

        mark(self.tags, prep_plus_infinitive)
        wsr = wording_syntactic_roles(self.syntactic_roles, self.tags)
        pred_finder(
            self.tags,
            self.semantic_roles,
            self.syntactic_roles,
            self.sem_roles_cov_subjects,
            potential_sub_obj,
        )

        result = {
            "sentence": self.sentence,
            "tags": self.tags,
            "original_tags": self.original_tags,
            "diatheses": get_diatheses(self.tags),
            "Candidates for subjects and direct objects": potential_sub_obj,
            "Syntactic functions": wsr,
            "sem_roles": self.semantic_roles,
            "Notes": self.notes,
        }
        return result

    def handle_diathesis(self, indici_proclisi, indici_verbi_flessi):
        mark_causative_fare(self.tags)
        for t in self.tags:
            if t.is_aux() and t.lemma == "avere":
                assign(self.tags, self.tags[t.get_same_block_indexes()[0]], "ACTIVE")
            elif (
                not t.is_aux() and not t.is_causative_fare and t.lemma in class_2_verbs
            ):
                assign(self.tags, self.tags[t.get_same_block_indexes()[0]], "MIDDLE_MR")
        pRFL(self.tags, indici_verbi_flessi, indici_proclisi, self.notes)
        passive(self.tags, self.notes)
        active_mRFL(self.tags)

    def get_tags(self, sentence: str, _save_sentence=False):
        if self._init:
            self.__init__()
        self.sentence = sentence
        if _save_sentence:
            save_sentence(sentence)
        tags = request_tags(sentence)
        self.tags = [Tag(t[0], t[1], t[2]) for t in tags]
        self.original_tags = [t.copy() for t in self.tags]  # tags originali
        for i, t in enumerate(self.tags):
            self.tags[i].index = i
            self.tags[i].all_tags = self.tags
        self._init = True


def entailment(sentence1: str, sentence2: str) -> Tuple[int, List, List, List]:
    tagger = NLPYTALY()
    res1 = tagger.tag(sentence1)
    res2 = tagger.tag(sentence2)
    rs1 = res1["sem_roles"]
    rs2 = res2["sem_roles"]

    if len(rs1) == 0 or len(rs1) == 0:
        return None, rs1, rs2, []

    acted_upon_roles = ["PASSIVE", "ACTIVE_SI"]

    def check_membership(rs, rs_list: List):
        for tmp in rs_list:
            if (
                rs.f1 == tmp.f1
                # vedere se è il caso di limitare il caso di acted upon solo alla classe 'bivalenti'
                and (
                    rs.f3 == tmp.f3
                    or (rs.f3 in acted_upon_roles and tmp.f3 in acted_upon_roles)
                )
                and (
                    rs.f2 == tmp.f2
                    or rs.f2[0] == tmp.f2[0]
                    # (insultare) < (insultare,parolacce)
                    and len(rs.f2) < len(tmp.f2)
                )
            ):
                return True
        return False

    def check_first_item_entailment(rs, rs_list: List):
        for tmp in rs_list:
            if (
                rs.f1 == tmp.f1
                and rs.f3 == tmp.f3
                and (
                    rs.f2 == tmp.f2
                    # # Colpire,pedate
                    # # Colpire,pugni
                    # or (
                    #     rs.f2[0] == tmp.f2[0]
                    #     and len(rs.f2) == len(tmp.f2)
                    #     and len(rs.f2) > 1
                    #     and len(tmp.f2) > 1
                    #     and rs.f2[1] != tmp.f2[1]
                    # )
                    # # Svolgere,professione,meccanico
                    # # Svolgere,professione,poliziotto
                    # or (
                    #     rs.f2[0] == tmp.f2[0]
                    #     and len(rs.f2) == len(tmp.f2)
                    #     and len(rs.f2) > 2
                    #     and len(tmp.f2) > 2
                    #     and rs.f2[2] != tmp.f2[2]
                    # )
                    # Confronto fino all'i-esimo elemento
                    # Colpire,pedate
                    # Colpire,pugni
                    # Svolgere,professione,meccanico
                    # Svolgere,professione,poliziotto
                    or any(
                        rs.f2[0] == tmp.f2[0]
                        and len(rs.f2) == len(tmp.f2)
                        and len(rs.f2) > i
                        and len(tmp.f2) > i
                        and rs.f2[i] != tmp.f2[i]
                        for i in range(1, len(rs.f2))
                    )
                )
            ):
                return True
        return False

    def check_common(rs1, rs2):
        common = list(set(rs1) & set(rs2))
        return common

    if all(check_membership(x, rs2) for x in rs1) and all(
        check_membership(x, rs1) for x in rs2
    ):
        return 0, rs1, rs2, []
    elif all(check_membership(x, rs2) for x in rs1):
        return 1, rs1, rs2, []
    elif all(check_membership(x, rs1) for x in rs2):
        return -1, rs1, rs2, []
    elif common := check_common(rs1, rs2):
        return 4, rs1, rs2, common
    elif all(check_first_item_entailment(x, rs2) for x in rs1) and all(
        check_first_item_entailment(x, rs1) for x in rs2
    ):
        common = []
        for tmp in rs1 + rs2:
            if len(tmp.f2) != 1:
                # eliminiamo l'ultimo elemento (diverso) per poter calcolare l'entailment
                del tmp.f2[-1]
            if tmp not in common:
                common.append(tmp)

        return 3, rs1, rs2, common  # 3rd party

    return None, rs1, rs2, []


if __name__ == "__main__":
    pass
