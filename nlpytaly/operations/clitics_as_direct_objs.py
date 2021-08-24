from typing import List

from ..Tag import Tag
from ..Utils import get_subj_obj_occurrences_for_tag
from ..data.clitics import clitics
from ..data.verbs.intransitives import all_intransitives


def clitics_as_dir_objs(tags: List[Tag], syntactic_roles) -> None:
    for t in tags:
        if t.is_in_SV_block():
            v_block = t.get_same_block_tags()
            if not any(x.lemma in all_intransitives for x in v_block):
                _, o, _, _ = get_subj_obj_occurrences_for_tag(t, tags, syntactic_roles)
                if not o and v_block[0].is_active():
                    for tag in v_block:
                        if tag.lemma in clitics and tag.lemma != "non":
                            syntactic_roles[(tag.index,)] = (
                                "OD",
                                t.get_same_block_indexes(),
                            )
