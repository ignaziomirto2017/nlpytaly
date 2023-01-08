from typing import Dict, Set

cognate_ate_multiwords: Dict[str, str] = {
    "bacchettate": "bacchettare",
    "bastonate": "bastonare",
    "cannonate": "cannoneggiare",
    "coltellate": "accoltellare",
    "cornate": "incornare",
    "frustate": "frustare",
    "manganellate": "manganellare",
    "morsi": "mordere",
    "pernacchie": "spernacchiare",
    "picconate": "picconare",
    "pizzichi": "pizzicare",
    "pizzicotti": "pizzicare",
    "pugnalate": "pugnalare",
    "randellate": "randellare",
    "schiaffetti": "schiaffeggiare",
    "schiaffi": "schiaffeggiare",
    "schiaffoni": "schiaffeggiare",
    "sculacciate": "sculacciare",
    "spinte": "spingere",
    "spintoni": "spingere",
    "sprangate": "sprangare",
    "stangate": "stangare",
    "strattonate": "strattonare",
    "strigliate": "strigliare",
}

ate_multiwords: Dict[str, str] = {
    "archibugiate": "sparare",  # il verbo è qui intransitivo (a chi si spara)
    "ceffoni": "schiaffeggiare",
    "dentate": "mordere",
    "fucilate": "sparare",  # esiste 'fucilare', ma con altro significato
    "manrovesci": "schiaffeggiare",
    "mitragliate": "sparare",
    "moschettate": "sparare",
    "pistolettate": "sparare",
    "revolverate": "sparare",
    "rivoltellate": "sparare",
    "sberle": "schiaffeggiare",
    "scapaccioni": "schiaffeggiare",
    "scappellotti": "schiaffeggiare",
    "schioppettate": "sparare",
    "sganassoni": "schiaffeggiare",
} | cognate_ate_multiwords

ate_multiwords_colpire: Set[str] = {
    "accettate",
    "ancate",
    "asciate",
    "badilate",
    "baionettate",
    "bicchierate",
    "bidonate",
    "borsate",
    "botte",
    "bottigliate",
    "calci",
    "calcioni",
    "capocciate",
    "cappellate",
    "catinellate",
    "cazzotti",  # 'scazzottare' esiste, ma dà reciproco
    "ciabattate",
    "ciaspolate",
    "cinghiate",
    "cipollate",
    "cocomerate",
    "colpi",
    "colubrinate",
    "craniate",
    "cucchiaiate",
    "culate",
    "cuscinate",
    "ditate",
    "forchettate",
    "forconate",
    "fornellate",
    "frecciate",
    "ginocchiate",
    "gomitate",
    "legnate",
    "manate",
    "martellate",
    "mazzolate",
    "mestolate",
    "nasate",
    "ombrellate",
    "pacche",
    "padellate",
    "pagaiate",
    "palate",
    "palettate",
    "pedate",
    "pietrate",
    "pinzate",
    "pomodorate",
    "prugnate",
    "pugni",
    "racchettate",
    "rasoiate",
    "roncolate",
    "sassate",
    "sassi",
    "scarpate",
    "schienate",
    "sciabolate",
    "scodellate",
    "scudisciate",
    "secchiate",
    "sgabellate",
    "spallate",
    "sportellate",
    "sputi",  # sputare = intransitive (ma 'sputare sangue')
    "stilettate",
    "testate",
    "unghiate",
    "vergate",
    "zampate",
    "zoccolate",
}

ate_multiwords_insultare: Set[str] = {
    "bestemmie",
    "ingiurie",
    "insulti",  # con controparte verbale
    "minacce",
    "offese",
    "parolacce",
    "parole",
    "sberleffi",
    "urla",  # urlare = intransitive
}


synonyms: Dict[str, str] = {
    "cazzotti": "pugni",
    "pedate": "calci",
    "spinte": "spintoni",
    "sassi": "sassate",
}

__joined__ = (
    list(cognate_ate_multiwords.keys())
    + list(ate_multiwords.keys())
    + list(ate_multiwords_colpire)
    + list(ate_multiwords_insultare)
)

if __name__ == "__main__":
    print(len(__joined__))
