from typing import List

from ...Tag import Tag


def role_found(tags: List[Tag], indexes, role, verb_indexes, dict_roles):
    for i in indexes:
        tags[i].syntactic_role = role
    # `indexes` ha il ruolo di `role` per il verbo `verb_indexes`
    dict_roles[indexes] = (role, verb_indexes)
