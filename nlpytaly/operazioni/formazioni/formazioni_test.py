from .formazione_infinito_riflessivo import formazione_infinito_riflessivo


def test01():
    assert formazione_infinito_riflessivo("giocare") == "giocarsi"
    assert formazione_infinito_riflessivo("essere") == "essersi"
    assert formazione_infinito_riflessivo("dire") == "dirsi"
    assert formazione_infinito_riflessivo("porre") == "porsi"
    assert formazione_infinito_riflessivo("astrarre") == "astrarsi"
