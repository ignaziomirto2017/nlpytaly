from typing import Set

# A Max piace il filetto
two_place_predicate2: Set[str] = {
    "aggradare",
    "appartenere",
    "capitare",
    "piacere",
    "venire",
    # TODO: to be completed
}

# con particella
class_2_verbs_si: Set[str] = {
    "abbioccare",
    "abbuffare",
    "accanire",
    "accaparrare",
    "accapigliare",
    "accapponare",
    "acciambellare",
    "accigliare",
    "accingere",
    "accoccolare",
    "accomiatare",
    "accomodare",
    "accorgere",
    "accovacciare",
    "acquattare",
    "addentrare",
    "addire",
    "affacciare",
    "affezionare",
    "affrettare",
    "aggrappare",
    "ammalare",
    "ammutinare",
    "appisolare",
    "apprestare",
    "appropriare",
    "arrabattare",
    "arrabbiare",
    "arrampicare",
    "arrendere",
    "arroccare",
    "arrogare",
    "arrovellare",
    "attagliare",
    "attardare",
    "atteggiare",
    "attenere",
    "avvalere",
    "avventare",
    "avventurare",
    "azzuffare",
    "baloccare",
    "barcamenare",
    "capacitare",
    "cimentare",
    "confare",
    "congratulare",
    "crogiolare",
    "defilare",
    "deflettere",
    "destreggiare",
    "dileguare",  # check
    "dimenare",
    "dimettere",
    "disamorare",
    "disinnamorare",
    "disperare",
    "ergere",
    "esimere",
    "estraniare",
    "felicitare",
    "fidare",
    "fiondare",
    "gingillare",
    "imbattere",
    "imbestialire",
    "imbronciare",
    "immedesimare",
    "impadronire",
    "impappinare",
    "impegolare",
    "impelagare",
    "impennare",
    "impicciare",
    "impigliare",
    "impipare",  # careful: come 'fregarsene' me ne impipo
    "impossessare",
    "impratichire",
    "incamminare",
    "incaponire",
    "incavolare",
    "inchinare",
    "industriare",
    "inerpicare",
    "infuriare",
    "ingegnare",
    "inginocchiare",
    "ingraziare",
    "inimicare",
    "innamorare",
    "intercorrere",
    "invaghire",
    "lambiccare",
    "lamentare",
    "librare",
    "ostinare",
    "pavoneggiare",
    "pentire",
    "piccare",
    "premurare",
    "raccapezzare",
    "rannicchiare",
    "ravvedere",
    "ribellare",
    "ricredere",
    "ripercuotere",
    "sbellicare",
    "sbizzarrire",
    "sbracciare",
    "scapicollare",
    "scervellare",
    "sconfinferare",
    "scontrare",
    "sdebitare",
    "sfaldare",
    "smagare",
    "sobbarcare",
    "soffermare",
    "sperdere",
    "spicciare",
    "stagliare",
    "stravaccare",
    "struggere",
    "susseguire",
    "svagare",
    "svignare",
    "trastullare",
    "vanagloriare",
    "vergognare",
}

# senza particella
class_2_verbs_: Set[str] = {
    "accadere",
    "accedere",
    "accorrere",
    "adontare",
    "affiorare",
    "affluire",
    "allibire",
    "ammattire",
    "ammontare",
    "ammuffire",
    "andare",
    "apparire",
    "appartenere",
    "appassire",
    "approdare",
    "ardere",
    "arretrare",
    "arrivare",
    "arrossire",
    "ascendere",
    "atterrare",
    "avvenire",
    "balenare",  # regge un 3 (ma... Max è a chi si balena)
    "baluginare",
    "balzare",
    "bastare",
    "bisognare",
    "cadere",
    "capitare",
    "cascare",
    "colare",
    "comparire",
    "competere",
    "confluire",
    "consistere",
    "constare",
    "convolare",
    "correre",
    "costare",
    "crashare",
    "crollare",
    "culminare",
    "decadere",
    "decedere",
    "decorrere",
    "decrescere",
    "defluire",
    "degenerare",
    "deperire",
    "derivare",
    "dilagare",
    "dimagrire",
    "dipendere",
    "discendere",
    "discernere",
    "divampare",
    "divenire",
    "divergere",
    "diventare",
    "dolere",
    "durare",
    "emergere",
    "emigrare",
    "entrare",
    "esistere",
    "evadere",
    "evaporare",
    "evolvere",
    "fioccare",
    "fiorire",
    "fluire",
    "franare",
    "fuggire",
    "fuoriuscire",
    "germinare",
    "giungere",
    "guizzare",
    "imbizzarrire",
    "imbolsire",
    "impallidire",
    "impazzare",
    "impazzire",
    "implodere",
    "incanutire",
    "incappare",
    "incespicare",
    "inciampare",
    "incombere",
    "incorrere",
    "insorgere",
    "intercorrere",
    "intervenire",
    "irrancidire",
    "irrompere",
    "mancare",
    "marcire",
    "migrare",
    "morire",
    "nascere",
    "occorrere",
    "parere",
    "partire",
    "perire",
    "pendere",
    "perdurare",
    "perire",
    "permanere",
    "persistere",
    "pertenere",
    "pervenire",
    "piombare",
    "precipitare",
    "prevalere",
    "provenire",
    "prudere",  # prende un 3
    "quagliare",
    "questionare",
    "rabbrividire",
    "refluire",
    "regredire",
    "resistere",
    "restare",
    "retrocedere",
    "riaccadere",
    "riappassire",
    "ricadere",
    "ricorrere",
    "ridiventare",
    "ridondare",
    "riemergere",
    "rientrare",
    "rifiorire",
    "rifuggire",
    "rimanere",
    "rimbombare",
    "rinascere",
    "rincasare",
    "rincrescere",
    "rinsavire",
    "ripartire",
    "risiedere",
    "risorgere",
    "risplendere",
    "risultare",
    "ritorcere",
    "ritornare",
    "riuscire",
    "ruzzolare",
    "salire",  # Leo sale le scale + Leo sale
    "sbiancare",
    "sboccare",
    "sbocciare",
    "sbollire",
    "sbottare",
    "sbucare",
    "scaciottare",
    "scadere",
    "scampare",
    "scappare",
    # "scattare", se inserito, blocca 'support verb'
    "scaturire",
    "scendere",  # Leo scende le scale + Leo scende
    "scemare",
    "schiattare",
    "scivolare",
    "scomparire",
    "scoppiare",
    "scorrere",
    "sembrare",
    "sfagiolare",
    "sfiorire",
    "sfociare",
    "sfrecciare",
    "sfuggire",
    "sgattaiolare",
    "sgattare",
    "sgorgare",
    "slittare",
    "sobbalzare",
    "soccombere",
    "soggiacere",
    "soggiungere",
    "sopraggiungere",
    "sopravvenire",
    "sopravvivere",
    "sorgere",
    "sortire",
    "sottostare",
    "sovvenire",
    "sparire",
    "spettare",
    "spiacere",
    "spirare",
    "stramazzare",
    "stridere",
    "subentrare",
    "succedere",
    "sussistere",
    "svanire",
    "svellere",
    "svenire",
    "tornare",
    "tracollare",
    "tramontare",
    "transitare",
    "trapelare",
    "trasalire",
    "trasecolare",
    "trasparire",
    "trasudare",
    "uscire",
    "valere",
    "vertere",
}

class_2_verbs: Set[str] = class_2_verbs_si | class_2_verbs_ | two_place_predicate2

if __name__ == "__main__":
    print(len(class_2_verbs))
