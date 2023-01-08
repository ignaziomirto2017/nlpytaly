from typing import List, Set, Tuple

from .data.synonyms import are_synonyms
from .data.verbs.class_1_verbs import two_place_predicate1
from .data.verbs.class_2_verbs import class_2_verbs, two_place_predicate2
from .data.verbs.intransitives import all_intransitives
from .data.verbs.trivalent import trivalent_verbs
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
from .operations.multiwords.multiwords import multiwords
from .operations.noun_verb_disambiguation import noun_verb_disambiguation
from .operations.place_marker import place_marker
from .operations.preposition_plus_infinitive import detect_prep_plus_infinitive
from .operations.search_sub_obj_candidates.handler import candidates_handler
from .operations.semantic_roles.causative_fare_construction import mark_causative_fare
from .operations.semantic_roles.job_fare_construction import mark_job_sem_role
from .operations.semantic_roles.PredFinder import mark, pred_finder
from .operations.semantic_roles.SemRole.SemRole import (
    AMBIGUOUS_SEM_ROLE,
    JOB_SEM_ROLE,
    SUPP_SEM_ROLE,
    AbstractSemRole,
    JobSemRole,
    SuppSemRole,
)
from .operations.semantic_roles.verb_support_construction import (
    mark_verb_support_construction,
)
from .operations.syntactic_roles.syntactic_roles import syntactic_roles
from .request_tags import request_tags
from .Tag import Tag
from .Utils import get_diatheses, save_sentence, wording_syntactic_roles


class NLPYTALY(object):
    def __init__(self):
        self._init = False

        self.tags: List[Tag] = []
        self.original_tags: List[Tag] = []

        self.sentence: str = ""

        self.syntactic_roles = {}
        self.semantic_roles: List[AbstractSemRole] = []

        self.notes: List[str] = []

    def tag(self, sentence: str):
        self.get_tags(sentence)
        multiwords(self.tags)
        occurence_corrections(self.tags)
        noun_verb_disambiguation(self.tags)

        self.set_max_no_assignable_sem_roles()

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
        self.handle_diathesis(proclisis_indexes, inflected_verbs_indexes)
        maybe_partitive(self.tags, self.notes)
        subj_exclusions = mark_verb_support_construction(self.tags)
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
                subj_exclusions,
                direct_obj_exclusions,
            )
        pi_occorrenze = []
        for index_block in prep_plus_infinitive:
            pi_occorrenze.append(
                " ".join([self.tags[x].occurrence for x in index_block])
            )

        mark(self.tags, prep_plus_infinitive)
        clitics_disambiguation(self.tags, inflected_verbs_indexes, self.syntactic_roles)
        wsr = wording_syntactic_roles(self.syntactic_roles, self.tags)
        pred_finder(
            self.tags, self.semantic_roles, self.syntactic_roles, potential_sub_obj
        )

        print("\nASSIGNED SEM ROLES")
        for t in self.tags:
            if t.is_verb():
                print(f"\t {t} {t.assigned_sem_roles}/{t.assignable_sem_roles}")

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

    def set_max_no_assignable_sem_roles(self):
        for t in self.tags:
            lemma = t.lemma
            if lemma in two_place_predicate1 | two_place_predicate2:
                t.set_max_assignable_sem_roles(2)
            elif lemma in all_intransitives:
                t.set_max_assignable_sem_roles(1)
            elif lemma in trivalent_verbs:
                t.set_max_assignable_sem_roles(3)
            else:
                t.set_max_assignable_sem_roles(2)

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
        self.remove_unverbal_sequences()
        for i, t in enumerate(self.tags):
            self.tags[i].index = i
            self.tags[i].all_tags = self.tags
        self._init = True

    def remove_unverbal_sequences(self):
        flag = False
        for i, t in enumerate(self.tags):
            if t.lemma == "," and flag:
                self.notes.append(
                    f"Removed sequence: {' '.join(x.occ for x in self.tags[flag:i+1])}"
                )
                self.tags = self.tags[0:flag] + self.tags[i + 1 :]
                break
            elif t.lemma == ",":
                flag = i
            elif t.is_verb():
                flag = False


def entailment(sentence1: str, sentence2: str) -> Tuple[int, List, List, List]:
    tagger = NLPYTALY()
    res1 = tagger.tag(sentence1)
    res2 = tagger.tag(sentence2)
    rs1 = res1["sem_roles"]
    rs2 = res2["sem_roles"]

    if len(rs1) == 0 or len(rs1) == 0:
        return None, rs1, rs2, []

    acted_upon_roles = ["PASSIVE", "ACTIVE_SI"]

    def check_membership(rs: AbstractSemRole, rs_list: List):
        for tmp in rs_list:
            tmp: AbstractSemRole
            if (
                # f1 field
                # io osservo la foto, io osservo la fotografia
                # strictly equal or synonyms
                (rs.f1 == tmp.f1 or are_synonyms(rs.f1, tmp.f1))
                # f2 field
                and (
                    # strictly equal
                    rs.f2 == tmp.f2
                    # first synonyms, length differs
                    # balzare, rapidamente => saltare
                    or (
                        (rs.f2[0] == tmp.f2[0] or are_synonyms(rs.f2[0], tmp.f2[0]))
                        # (insultare) < (insultare, parolacce)
                        and len(rs.f2) < len(tmp.f2)
                    )
                    # same lenght, all synonyms
                    # balzare, rapidamente = saltare, velocemente
                    or (
                        len(rs.f2) == len(tmp.f2)
                        and all(
                            # this should act on lemmas, not on strings
                            # maybe save f2 tags too?
                            are_synonyms(rs.f2[i], tmp.f2[i])
                            for i in range(len(rs.f2))
                        )
                    )
                )
                # f3 field (tense)
                # stricly equal except for special cases
                # (http://localhost:3000/semroles/Il%20cane%20innervosisce%20Piero.%20Piero%20%C3%A8%20innervosito)
                # vedere se è il caso di limitare il caso di acted upon solo alla classe 'bivalenti'
                and (
                    rs.f3 == tmp.f3
                    or (rs.f3 in acted_upon_roles and tmp.f3 in acted_upon_roles)
                    or (hasattr(rs, "embedder") or hasattr(tmp, "embedder"))
                )
            ):
                return True
        return False

    def check_common(rs1: List, rs2: List):
        common = {"list": [], "features": []}
        common_list = common["list"]
        common_features = common["features"]
        joined: List = rs1 + rs2
        for rs in joined:
            if rs in rs1 and rs in rs2:
                if rs.f4 == AMBIGUOUS_SEM_ROLE:
                    if rs in common_list:
                        common_list.remove(rs)
                        common_list.append(rs)
                elif rs.f4 == JOB_SEM_ROLE:
                    rs: JobSemRole
                    rs_copy = rs.copy()
                    rs_copy.f2.pop()
                    common_list.append(rs_copy) if rs not in common_list else None
                elif rs.f4 == SUPP_SEM_ROLE and len(rs.f2) > 1:
                    rs: SuppSemRole
                    if rs not in common_list:
                        common_list.append(rs)
                    else:
                        existing = common_list[common_list.index(rs)]
                        tmp = set(rs.f2[1:]) & set(existing.f2[1:])
                        if tmp:
                            common_features.append(tmp)
                else:
                    common_list.append(rs) if rs not in common_list else None

        return common

    common_empty = {"list": [], "features": []}

    def all_negative(sem_roles: List[AbstractSemRole]):
        return all(x.is_negative() for x in sem_roles)

    def all_positive(sem_roles: List[AbstractSemRole]):
        return all(x.is_positive() for x in sem_roles)

    if (
        len(rs1) == len(rs2)
        and all(check_membership(x, rs2) for x in rs1)
        and all(check_membership(x, rs1) for x in rs2)
    ):
        if (all_positive(rs1) and all_positive(rs2)) or (
            all_negative(rs1) and all_negative(rs2)
        ):
            return 0, rs1, rs2, common_empty
        else:
            return None, rs1, rs2, {"list": [], "features": []}
    elif all(check_membership(x, rs2) for x in rs1):
        if all_positive(rs1) and all_positive(rs2):
            return 1, rs1, rs2, common_empty
        else:
            return None, rs1, rs2, {"list": [], "features": []}
    elif all(check_membership(x, rs1) for x in rs2):
        if all_positive(rs1) and all_positive(rs2):
            return -1, rs1, rs2, common_empty
        else:
            return None, rs1, rs2, {"list": [], "features": []}
    else:
        common = check_common(rs1, rs2)
        if common["list"]:
            return 4, rs1, rs2, common

    return None, rs1, rs2, {"list": [], "features": []}


def entailment_f2f3(sem_roles1, sem_roles2) -> Tuple[int, Set[str]]:
    rs1c = set(rs.code for rs in sem_roles1)
    rs2c = set(rs.code for rs in sem_roles2)

    intersection = rs1c.intersection(rs2c)

    if rs1c == rs2c:
        return 0, intersection
    elif rs1c.issubset(rs2c):
        return 1, intersection
    elif rs2c.issubset(rs1c):
        return 2, intersection
    elif len(intersection) != 0:
        return 3, intersection
    return None, intersection


if __name__ == "__main__":
    pass
