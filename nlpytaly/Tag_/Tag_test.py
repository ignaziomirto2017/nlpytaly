from typing import List

import pytest

from ..nlpytaly import NLPYTALY
from . import Tag


@pytest.fixture()
def tagger():
    return NLPYTALY()


def test1(tagger):
    tagger.tag("Le foto non le erano ancora state fatte dal marito")
    tags: List[Tag] = tagger.tags

    foto = tags[1]
    assert foto.is_in_SN_block()
    erano = tags[4]
    assert erano.is_in_SV_block()
