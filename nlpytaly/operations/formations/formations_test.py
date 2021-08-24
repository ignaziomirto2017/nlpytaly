from .reflexive_infinitive_formation import reflexive_infinitive_formation


def test01():
    assert reflexive_infinitive_formation("giocare") == "giocarsi"
    assert reflexive_infinitive_formation("essere") == "essersi"
    assert reflexive_infinitive_formation("dire") == "dirsi"
    assert reflexive_infinitive_formation("porre") == "porsi"
    assert reflexive_infinitive_formation("astrarre") == "astrarsi"
    assert reflexive_infinitive_formation("addurre") == "addursi"
