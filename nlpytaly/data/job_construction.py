from typing import List, Set

with open(str(__file__).strip(".py") + "_list.txt") as f:
    job_list: List[str] = f.readlines()
    job_list: Set[str] = set(map(lambda x: x.strip(), job_list))
