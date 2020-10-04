def set_pn(self, p: int, n: str):
    self.set_p(p)
    self.set_n(n)


def set_gn(self, g, n):
    self.genere = g
    self.numero = n


def set_n(self, n: str):
    if n in ["s", "p", "s|p"]:
        self.numero = n
    else:
        raise ValueError()


def set_g(self, g: str):
    if g in ["m", "f", "m|f"]:
        self.genere = g
    else:
        raise ValueError()


def set_p(self, p: int):
    first_person = "1st"
    second_person = "2nd"
    third_person = "3rd"
    amb_1_2_3 = "1st|2nd|3rd"
    amb_1_3 = "1st|3rd"
    if p == 1:
        self.persona = first_person
    elif p == 2:
        self.persona = second_person
    elif p == 3:
        self.persona = third_person
    elif p == 13:
        self.persona = amb_1_3
    elif p == 123:
        self.persona = amb_1_2_3
    else:
        raise ValueError()
