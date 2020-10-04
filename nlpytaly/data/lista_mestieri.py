# coding=utf-8
from typing import List, Set

with open(str(__file__).strip(".py") + ".txt") as f:
    lista_mestieri: List[str] = f.readlines()
    lista_mestieri: Set[str] = set(map(lambda x: x.strip(), lista_mestieri))
