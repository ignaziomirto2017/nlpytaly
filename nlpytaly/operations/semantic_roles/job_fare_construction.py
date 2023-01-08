from typing import List

from nlpytaly.operations.semantic_roles.utils import assign_and_increment

from ...data.definite_articles import definite_articles
from ...data.job_construction import job_list
from ...Tag import Tag
from ...Utils import increment_blocks, mark_tag
from .pred_assigners import pred_sem_mest, pred_syn_mest
from .SemRole.SemRole import JobSemRole


def mark_job_sem_role(tags: List[Tag]) -> List[int]:
    direct_obj_exclusions: List[int] = []
    for t in tags:
        prev = t.prev()
        if t.lemma in job_list and prev and prev.occ in definite_articles:
            for p in reversed(t.get_prev_block_tags()):
                # distanza tra nome del mestiere e fare
                if p.lemma == "fare":
                    fare_v_block = p.get_same_block_tags()
                    if (
                        fare_v_block
                        and fare_v_block[-1].is_infinitive()
                        and fare_v_block[-1].lemma != "fare"
                    ):
                        break
                    mark_tag(p, pred_syn_mest, t)
                    p.set_max_assignable_sem_roles(1)
                    mark_tag(t, pred_sem_mest, p)
                    direct_obj_exclusions.append(t.index)
                    increment_blocks(tags, t.index - 1, t.index)
                    break

    return direct_obj_exclusions


def assign_job_sem_role(sem_roles, sogg, t, v):
    sogg = [Tag(t.cov_sub, "-", "-")] if (not sogg) else sogg
    if t.is_active():
        assign_and_increment(
            t, JobSemRole(" ".join(x.occ for x in sogg), v.occ), sem_roles
        )
