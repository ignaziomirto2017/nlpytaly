_no_isc = [
    "acconsentire",
    "apparire",
    "applaudire",
    "aprire",
    "avvenire",
    "avvertire",
    "compire",
    "contravvenire",
    "convenire",
    "convenire",
    "coprire",
    "divertire",
    "dormire",
    "fuggire",
    "inghiottire",
    "inseguire",
    "inseguire",
    "intervenire",
    "investire",
    "mentire",
    "morire",
    "nutrire",
    "offrire",
    "partire",
    "pentire",
    "pervenire",
    "plaudire",
    "presentire",
    "proseguire",
    "riaprire",
    "ricoprire",
    "ricucire",
    "riempire",
    "rinvenire",
    "risalire",
    "riscoprire",
    "riuscire",
    "rivestire",
    "salire",
    "scomparire",
    "scoprire",
    "seguire",
    "sentire",
    "servire",
    "sfuggire",
    "soffrire",
    "susseguire",
    "svenire",
    "udire",
    "uscire",
    "venire",
    "vestire",
]


def third_person_formation(inf: str, include_si=False):
    r = ""
    inf = inf.lower()
    if inf == "dare":
        r = "dà"
    elif inf == "essere":
        r = "è"
    elif inf == "avere":
        r = "ha"
    elif inf == "bere":
        r = "beve"
    elif inf == "potere":
        r = "può"
    elif inf == "sapere":
        r = "sa"
    elif inf == "dovere":
        r = "deve"
    elif inf == "rifare":
        r = "rifà"
    elif inf == "dire":
        r = "dice"
    elif inf == "disdire":
        r = "disdice"
    elif inf == "morire":
        r = "muore"
    elif inf == "andare":
        r = "va"
    elif inf == "riandare":
        r = "riva"
    elif inf == "benedire":
        r = "benedice"
    elif inf == "comparire":
        r = "compare"
    elif inf.endswith("olere"):
        r = inf.replace("olere", "uole")
    elif inf.endswith("eguire"):
        r = inf.replace("ire", "e")
    elif inf.endswith("arre"):  # attrarre
        r = inf.replace("rre", "e")
    elif inf.endswith("urre"):
        r = inf.replace("urre", "uce")
    elif inf.endswith("tenere"):
        r = inf.replace("tenere", "tiene")
    elif inf.endswith("sedere"):
        r = inf.replace("sedere", "siede")
    elif inf.endswith("uscire"):
        r = inf.replace("uscire", "esce")
    elif inf.endswith("venire"):
        r = inf.replace("venire", "viene")
    elif inf.endswith("ire") and inf not in _no_isc:
        r = inf.replace("ire", "isce")
    elif inf.endswith("orre"):
        r = inf.replace("rre", "ne")
    else:
        if inf.endswith("ere") or inf.endswith("are"):
            r = inf[:-2]
        elif inf.endswith("ire"):
            if inf.endswith("empire"):
                r = inf.replace("ire", "ie")
            else:
                r = inf.replace("ire", "e")
    return "si " + r if include_si else r
