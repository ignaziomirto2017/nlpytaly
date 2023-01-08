from typing import List


def delete_candidate(result, candidato):
    """
    delete_candidate(result, [4])
    """
    for blocco_non_verb in result:
        blocco_non_verb: List
        if candidato in blocco_non_verb:
            blocco_non_verb.remove(candidato)
