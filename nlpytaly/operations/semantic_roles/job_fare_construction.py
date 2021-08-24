from typing import List

from .SemRole.SemRole import JobSemRole
from .pred_assigners import *
from ...Tag import Tag
from ...Utils import increment_blocks
from ...Utils import mark_tag
from ...data.definite_articles import definite_articles
from ...data.job_construction import job_list


def mark_job_sem_role(tags: List[Tag]) -> List[int]:
    direct_obj_exclusions: List[int] = []
    for t in tags:
        if t.lemma in job_list and tags[t.index - 1].occurrence in definite_articles:
            for p in reversed(t.get_prev_block_tags()):
                # distanza tra nome del mestiere e fare
                if p.lemma == "fare":
                    fare_v_block = p.get_same_block_tags()
                    if fare_v_block and fare_v_block[-1].is_infinitive():
                        break
                    mark_tag(p, pred_syn_mest, t)
                    mark_tag(t, pred_sem_mest, p)
                    direct_obj_exclusions.append(t.index)
                    increment_blocks(tags, t.index - 1, t.index)
                    break

    return direct_obj_exclusions


def assign_job_sem_role(sem_roles, sogg, t, v):
    if t.is_active():
        if sogg and sogg[0].sem_role_allowed(t.get_same_block_indexes()):
            sem_roles.append(JobSemRole(" ".join(x.occ for x in sogg), v.occ))
