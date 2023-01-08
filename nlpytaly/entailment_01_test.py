from nlpytaly import entailment
from nlpytaly.operations.semantic_roles.SemRole.consts import ACTV, ACTV_S, PASSV
from nlpytaly.operations.semantic_roles.SemRole.SemRole import (
    DativeSemRole,
    OrdinarySemRole,
)
from nlpytaly.operations.semantic_roles.utils import list_equals_no_order

from .Test_utils import (
    entail_each_other,
    entailment,
    first_entails_second,
    in_common,
    mutual_entailment,
    no_entailment,
    one_way_entailment,
    second_entails_first,
)


def test1():
    res, rs1, rs2, common = entailment(
        "Le maestre prendono a bacchettate i bambini",
        "I bambini sono presi a bacchettate",
    )
    assert res == first_entails_second


def test2():
    res, rs1, rs2, common = entailment("Mario ha mangiato la pasta", "Mario canta")
    assert res is no_entailment


def test3():
    res, rs1, rs2, common = entailment(
        "Mario insulta l'amico", "Mario ha preso a parolacce l'amico"
    )
    assert res == second_entails_first


def test4():
    res, rs1, rs2, common = entailment(
        "Mario ha preso a cazzotti l'amico", "Mario ha colpito l'amico"
    )
    assert res == first_entails_second


def test5():
    res, rs1, rs2, common = entailment(
        "Mario ha preso a cazzotti l'amico", "Mario ha preso a pedate l'amico"
    )
    assert res == in_common
    expected_common = [
        OrdinarySemRole("MARIO", ["COLPIRE"], ACTV),
        OrdinarySemRole("L' AMICO", ["COLPIRE"], PASSV),
    ]
    for ec in expected_common:
        assert ec in common["list"]
    assert len(common["list"]) == len(expected_common)


def test6():
    res, rs1, rs2, common = entailment(
        "Mario ha fatto visitare il bambino dal medico", "Il medico visita il bambino"
    )
    assert res == first_entails_second


def test7():
    res, rs1, rs2, common = entailment(
        "Mario fa il meccanico", "Mario fa il poliziotto"
    )
    assert res == in_common


def test8():
    res, rs1, rs2, common = entailment(
        "Mario ha preso a cazzotti l'amico", "Mario ha preso a pugni l'amico"
    )
    assert res == mutual_entailment


def test9():
    res, rs1, rs2, common = entailment(
        "La pasta è mangiata da Antonio", "Antonio mangia la pasta"
    )
    assert res == mutual_entailment


def test10():
    res, rs1, rs2, common = entailment(
        "Mario ha messo Luigi sotto accusa", "Mario ha accusato Luigi"
    )
    assert res == mutual_entailment


def test11():
    res, rs1, rs2, common = entailment(
        "Mario ha comprato il gelato al bambino", "Mario ha comprato il gelato"
    )
    assert res == first_entails_second


def test12():
    res, rs1, rs2, common = entailment(
        "L'amico prende a cazzotti Antonio", "L'amico prende a pugni Antonio"
    )
    assert res == mutual_entailment


def test13():
    res, rs1, rs2, common = entailment(
        "Mario ha fatto bacchettare gli amici dal preside",
        "Il preside ha bacchettato gli amici",
    )
    assert res == first_entails_second


def test14():
    res, rs1, rs2, common = entailment(
        "Leonardo ha fatto arrabbiare l'amico", "L'amico si arrabbia"
    )
    assert res == first_entails_second


def test15():
    res, rs1, rs2, common = entailment(
        "Leonardo ha fatto mettere sotto accusa il tecnico dall'avvocato",
        "L'avvocato ha messo sotto accusa il tecnico",
    )
    assert res == first_entails_second


def test16():
    res, rs1, rs2, common = entailment(
        "Leonardo ha fatto mettere sotto accusa il tecnico dall'avvocato",
        "L'avvocato accusa il tecnico",
    )
    assert res == first_entails_second


def test17():
    res, rs1, rs2, common = entailment(
        "Il comandante ha fatto mettere agli arresti il ladro dal sergente",
        "Il ladro è stato arrestato dal sergente",
    )
    assert res == first_entails_second


def test18():
    res, rs1, rs2, common = entailment(
        "L'uomo aggredito ha denunciato gli assalitori", "Si aggredì l'uomo"
    )
    assert res == first_entails_second


def test19():
    res, rs1, rs2, common = entailment(
        "Il professore prende la ragazza a pugni",
        "Il professore prende la ragazza a sassate",
    )
    assert res == in_common
    expected_common = [
        OrdinarySemRole("IL PROFESSORE", ["COLPIRE"], ACTV),
        OrdinarySemRole("LA RAGAZZA", ["COLPIRE"], PASSV),
    ]
    for ec in expected_common:
        assert ec in common["list"]
    assert len(common["list"]) == len(expected_common)


def test20():
    res, rs1, rs2, common = entailment("Mario ha fatto un errore", "Mario ha sbagliato")
    assert res == mutual_entailment


def test21():
    res, rs1, rs2, common = entailment(
        "La polizia ha messo agli arresti il ragazzo",
        "La polizia ha messo in arresto il ragazzo",
    )
    assert res == mutual_entailment


def test22():
    res, rs1, rs2, common = entailment(
        "La polizia ha messo agli arresti il ragazzo",
        "La polizia ha arrestato il ragazzo",
    )
    assert res == mutual_entailment


def test23():
    res, rs1, rs2, common = entailment(
        "La polizia ha messo agli arresti il ragazzo",
        "Il ragazzo è stato arrestato dalla polizia",
    )
    assert res == mutual_entailment


def test24():
    res, rs1, rs2, common = entailment(
        "La polizia ha messo agli arresti il ragazzo", "Si è arrestato il ragazzo"
    )
    assert res == first_entails_second


def test25():
    res, rs1, rs2, common = entailment(
        "La procura ha fatto arrestare il ragazzo dalla polizia",
        "Si è arrestato il ragazzo",
    )
    assert res == first_entails_second


def test26():
    res, rs1, rs2, common = entailment(
        "Il medico fa deambulare il paziente", "Il paziente deambula"
    )
    assert res == first_entails_second


def test27():
    res, rs1, rs2, common = entailment(
        "La donna fece intervenire la sorella", "Intervenne la sorella"
    )
    assert res == first_entails_second


def test28():
    res, rs1, rs2, common = entailment(
        "Luca fece giocare l'asso a Piero", "Piero gioca l'asso"
    )
    assert res == first_entails_second


def test29():
    res, rs1, rs2, common = entailment(
        "L'amico è stato preso a parolacce", "L'amico è stato insultato"
    )
    assert res == first_entails_second


def test30():
    res, rs1, rs2, common = entailment(
        "La nostra cara amica si è fatta prestare dei libri dallo zio",
        "Lo zio ha prestato dei libri alla nostra cara amica",
    )
    assert res == first_entails_second


def test31():
    res, rs1, rs2, common = entailment(
        "Mario ha fatto fare un sorriso a Giulia", "Giulia ha sorriso"
    )
    assert res == first_entails_second


def test32():
    res, rs1, rs2, common = entailment(
        "Mario ha fatto fare un sorriso a Giulia", "Mario ha fatto sorridere Giulia"
    )
    assert res == mutual_entailment


def test33():
    res, rs1, rs2, common = entailment(
        "Mario ha fatto fare un sorriso a Giulia",
        "Giulia è stata fatta sorridere da Mario",
    )
    assert res == mutual_entailment


def test34():
    res, rs1, rs2, common = entailment("Piero sorride a Lucia", "Piero fa un sorriso")
    assert res == first_entails_second


def test35():
    res, rs1, rs2, common = entailment(
        "Piero sorride a Lucia", "Piero fa un sorriso a Lucia"
    )
    assert res == mutual_entailment


def test36():
    res, rs1, rs2, common = entailment(
        "La mamma ha fatto accompagnare il bambino dalla nonna",
        "Il bambino si è fatto accompagnare dalla nonna",
    )
    assert res == in_common
    expected_common = [
        OrdinarySemRole("LA NONNA", ["accompagnare"], ACTV),
        OrdinarySemRole("IL BAMBINO", ["accompagnare"], PASSV),
    ]
    for ec in expected_common:
        assert ec in common["list"]
    assert len(common["list"]) == len(expected_common)


def test37():
    res, rs1, rs2, common = entailment(
        "Mario ha accumulato i debiti", "I debiti si accumulano"
    )
    assert res == first_entails_second


def test38():
    res, rs1, rs2, common = entailment(
        "Io mi sono fatto accompagnare da Luca", "Luca ha accompagnato me"
    )
    assert res == first_entails_second


def test39():
    res, rs1, rs2, common = entailment(
        "Mario ha visto me", "Io sono stato visto da Mario"
    )
    assert res == mutual_entailment


def test40():
    res, rs1, rs2, common = entailment(
        "Tu ti fai accompagnare da Luca", "Luca ha accompagnato te"
    )
    assert res == first_entails_second


def test41():
    res, rs1, rs2, common = entailment(
        "Mario ha visto te", "Tu sei stato visto da Mario"
    )
    assert res == mutual_entailment


def test42():
    res, rs1, rs2, common = entailment(
        "Essi si sono fatti accompagnare da Luca", "Luca ha accompagnato loro"
    )
    assert res == first_entails_second


def test43():
    res, rs1, rs2, common = entailment(
        "Essi hanno visto Mario", "Mario è stato visto da loro"
    )
    assert res == in_common
    expected_common = [OrdinarySemRole("MARIO", ["VEDERE"], PASSV)]
    list_equals_no_order(expected_common, common["list"])


def test44():
    res, rs1, rs2, common = entailment(
        "Piero ha addormentato i bambini", "I bambini si sono addormentati"
    )
    assert res == first_entails_second


def test45():
    res, rs1, rs2, common = entailment(
        "Voi fate venire quella donna.", "Quella donna viene."
    )
    assert res == first_entails_second


def test46():
    res, rs1, rs2, common = entailment("Mangi la pasta.", "La pasta è mangiata da te.")
    assert res == mutual_entailment


def test47():
    res, rs1, rs2, common = entailment("Salutai Mario.", "Io salutai Mario.")
    assert res == mutual_entailment


def test48():
    res, rs1, rs2, common = entailment("Ho visto loro.", "Loro furono visti da me.")
    assert res == mutual_entailment


def test49():
    res, rs1, rs2, common = entailment(
        "Il magistrato ha fatto mettere sotto sorveglianza gli indagati.",
        "Gli indagati sono sorvegliati.",
    )
    assert res == first_entails_second


def test51():
    res, rs1, rs2, common = entailment(
        "Il meccanismo si è inceppato", "Il meccanismo è inceppato"
    )
    assert res == mutual_entailment


def test52():
    res, rs1, rs2, common = entailment(
        "La ruggine ha inceppato l'arma.", "L'arma si inceppa."
    )
    assert res == first_entails_second


def test53():
    res, rs1, rs2, common = entailment(
        "Io ho prescritto a Piero una terapia antibiotica",
        "Ho prescritto una terapia antibiotica a Piero",
    )
    assert res == mutual_entailment


def test54():
    res, rs1, rs2, common = entailment(
        "Mario ha incoraggiato l'amico", "Mario ha dato coraggio all'amico"
    )
    assert res == mutual_entailment


def test55():
    res, rs1, rs2, common = entailment(
        "La maestra spera", "La maestra nutre una speranza"
    )
    assert res == mutual_entailment


def test56():
    res, rs1, rs2, common = entailment(
        "Sara si è fatta pettinare i capelli dalla mamma",
        "La mamma ha pettinato i capelli a Sara",
    )
    assert res == first_entails_second


def test57():
    res, rs1, rs2, common = entailment(
        "Mario ha fatto fare un balzo a Giulia", "Mario ha fatto balzare Giulia"
    )
    assert res == mutual_entailment


def test58():
    res, rs1, rs2, common = entailment(
        "Una task force ha fatto un'incursione in territorio sovietico",
        "Una task force penetra in territorio sovietico",
    )
    assert res == first_entails_second


def test59():
    res, rs1, rs2, common = entailment(
        "Voi faceste arrestare l'uomo alla donna", "Faceste arrestare l'uomo alla donna"
    )
    assert res == mutual_entailment


def test60():
    res, rs1, rs2, common = entailment(
        "I ragazzi sono stati presi a bacchettate", "i ragazzi bacchettati"
    )
    assert res == mutual_entailment


def test61():
    res, rs1, rs2, common = entailment(
        "Questa politica economica indebita lo Stato", "Lo stato si indebita"
    )
    assert res == first_entails_second


def test62():
    res, rs1, rs2, common = entailment(
        "Mario ha dato la cartellina alla sorella", "Mario dà la cartellina"
    )
    assert res == first_entails_second


def test63():
    res, rs1, rs2, common = entailment("Piero si è distratto", "Piero è distratto")
    assert res == mutual_entailment


def test64():
    res, rs1, rs2, common = entailment(
        "Sandro ha distratto Piero", "Piero si è distratto"
    )
    assert res == first_entails_second


def test65():
    res, rs1, rs2, common = entailment("Sandro ha distratto Piero", "Piero è distratto")
    assert res == first_entails_second


def test66():
    res, rs1, rs2, common = entailment(
        "Sandro ha impietosito Piero", "Piero si è impietosito"
    )
    assert res == first_entails_second


def test67():
    res, rs1, rs2, common = entailment(
        "Marco inebetisce Luca", "Luca è stato inebetito da Marco"
    )
    assert res == mutual_entailment


def test68():
    res, rs1, rs2, common = entailment("Marco inebetisce Luca", "Luca si è inebetito")
    assert res == first_entails_second


def test69():
    res, rs1, rs2, common = entailment(
        "Il magistrato ha fatto mettere sotto sorveglianza gli indagati",
        "Gli indagati sono sorvegliati",
    )
    assert res == first_entails_second


def test70():
    res, rs1, rs2, common = entailment(
        "Il magistrato ha fatto mettere gli indagati sotto sorveglianza dalla polizia",
        "La polizia sorveglia gli indagati",
    )
    assert res == first_entails_second


def test71():
    res, rs1, rs2, common = entailment(
        "Sandro ha preso a cazzotti Giulio", "Giulio è stato preso a legnate da Sandro"
    )

    assert res == in_common
    expected_common = [
        OrdinarySemRole("SANDRO", ["COLPIRE"], ACTV),
        OrdinarySemRole("GIULIO", ["COLPIRE"], PASSV),
    ]
    for ec in expected_common:
        assert ec in common["list"]
    assert len(common["list"]) == len(expected_common)


def test72():
    res, rs1, rs2, common = entailment("Ho riempito la vasca", "La vasca si è riempita")
    assert res == first_entails_second


def test73():
    res, rs1, rs2, common = entailment(
        "Leonardo fece aprire la porta a Maria da Luca",
        "Leonardo fece aprire la porta a Maria",
    )
    assert res == first_entails_second


def test74():
    res, rs1, rs2, common = entailment(
        "Leonardo fece aprire la porta a Maria da Luca",
        "Leonardo fece aprire la porta da Luca",
    )
    assert res == first_entails_second


def test75():
    res, rs1, rs2, common = entailment(
        "Leonardo fece aprire la porta a Maria da Luca", "Leonardo fece aprire la porta"
    )
    assert res == first_entails_second


def test76():
    res, rs1, rs2, common = entailment(
        "Leonardo fece aprire la porta a Maria da Luca", "Leonardo fece aprire"
    )
    assert res == first_entails_second


def test77():
    res, rs1, rs2, common = entailment(
        "Leonardo si fece aprire la porta da Luca", "Leonardo fece aprire la porta"
    )
    assert res == first_entails_second


def test78():
    res, rs1, rs2, common = entailment(
        "Sandra ha fatto pettinare Stefania da Luigi",
        "Stefania è stata fatta pettinare da Sandra",
    )
    assert res == first_entails_second


def test79():
    res, rs1, rs2, common = entailment(
        "Sandra ha fatto pettinare Stefania",
        "Stefania è stata fatta pettinare da Sandra",
    )
    assert res == mutual_entailment


def test80():
    res, rs1, rs2, common = entailment(
        "L'autista ha fermato la macchina", "La macchina si è fermata"
    )
    assert res == first_entails_second


def test81():
    res, rs1, rs2, common = entailment(
        "La lezione ha fatto rincretinire gli studenti", "Gli studenti rincretiniscono"
    )
    assert res == first_entails_second


def test82():
    res, rs1, rs2, common = entailment(
        "La lezione ha rincretinito gli studenti", "Gli studenti rincretiniscono"
    )
    assert res == first_entails_second


def test83():
    res, rs1, rs2, common = entailment(
        "Mario ha corso un rischio", "Mario ha corso un pericolo"
    )
    assert res == mutual_entailment


def test84():
    res, rs1, rs2, common = entailment(
        "Piero ha confuso gli spettatori", "Gli spettatori sono confusi"
    )
    assert res == first_entails_second


def test85():
    res, rs1, rs2, common = entailment(
        "Sandro indispettisce i ragazzi", "I ragazzi sono indispettiti"
    )
    assert res == first_entails_second


def test86():
    res, rs1, rs2, common = entailment(
        "Giulia ha fatto dare i documenti a Sara da Marco",
        "Marco ha dato i documenti a Sara",
    )
    assert res == first_entails_second


def test87():
    res, rs1, rs2, common = entailment(
        "Giulia ha fatto dare i documenti a Sara da Marco",
        "Marco ha dato i documenti a Sara",
    )
    assert res == first_entails_second


def test88():
    res, rs1, rs2, common = entailment(
        "Piero ha dato i regali alle bambine", "Alle bambine furono dati i regali"
    )
    assert res == first_entails_second


def test89():
    res, rs1, rs2, common = entailment(
        "L'amico è stato preso a parolacce da Mario", "Mario ha insultato l'amico"
    )
    assert res == first_entails_second


def test90():
    res, rs1, rs2, common = entailment(
        "Mario ha accumulato i debiti", "I debiti si sono accumulati"
    )
    assert res == first_entails_second


def test91():
    res, rs1, rs2, common = entailment(
        "La maestra ha rivolto la parola allo scolaro", "La maestra parla"
    )
    assert res == first_entails_second


def test92():
    res, rs1, rs2, common = entailment(
        "La maestra ha rivolto la parola allo scolaro",
        "La maestra ha parlato allo scolaro",
    )
    assert res == mutual_entailment


def test93():
    res, rs1, rs2, common = entailment(
        "Il pubblico applaudì il cantante", "Il pubblico fece un applauso al cantante"
    )
    assert res == mutual_entailment


def test94():
    res, rs1, rs2, common = entailment("Lui mi ha visto", "Lui ha visto me")
    assert res == mutual_entailment


def test95():
    res, rs1, rs2, common = entailment("Mi ha visto", "Ha visto me")
    assert res == mutual_entailment


def test96():
    res, rs1, rs2, common = entailment("Mario ha paura", "Mario è impaurito")
    assert res == mutual_entailment


def test97():
    res, rs1, rs2, common = entailment("Vedo lei", "La vedo")
    assert res == mutual_entailment


def test98():
    res, rs1, rs2, common = entailment("Mario ha risolto il caso", "Il caso è risolto")
    assert res == first_entails_second


def test99():
    res, rs1, rs2, common = entailment(
        "Mario ha risolto il caso", "Il caso si è risolto"
    )
    assert res == first_entails_second


def test100():
    res, rs1, rs2, common = entailment(
        "Il tenente si è rimboccato le maniche",
        "Il tenente ha rimboccato le maniche al collega",
    )
    assert res == in_common
    expected_common = [
        OrdinarySemRole("Il tenente", ["rimboccare"], ACTV),
        OrdinarySemRole("le maniche", ["rimboccare"], PASSV),
    ]
    for ec in expected_common:
        assert ec in common["list"]
    assert len(common["list"]) == len(expected_common)


def test101():
    res, rs1, rs2, common = entailment(
        "La mamma ha fatto mangiare a Gianni la pasta",
        "La pasta è stata mangiata da Gianni",
    )
    assert res == first_entails_second


def test102():
    res, rs1, rs2, common = entailment(
        "Faccio il professore", "Io faccio il professore"
    )
    assert res == mutual_entailment


def test103():
    res, rs1, rs2, common = entailment(
        "Io ho fatto passeggiare il cane", "Io ho fatto fare una passeggiata al cane"
    )
    assert res == mutual_entailment


def test104():
    res, rs1, rs2, common = entailment(
        "Ho fatto passeggiare il cane", "Io ho fatto fare una passeggiata al cane"
    )
    assert res == mutual_entailment


def test105():
    res, rs1, rs2, common = entailment("Io ho fatto una cura", "Ho fatto una cura")
    assert res == mutual_entailment


def test106():
    res, rs1, rs2, common = entailment(
        "Diamo un abbraccio ai ragazzi", "Noi diamo un abbraccio ai ragazzi"
    )
    assert res == mutual_entailment


def test107():
    res, rs1, rs2, common = entailment(
        "Diamo manforte a Luigi", "Noi diamo aiuto a Luigi"
    )
    assert res == mutual_entailment


def test108():
    res, rs1, rs2, common = entailment(
        "Diamo manforte a Luigi", "Noi diamo un aiuto a Luigi"
    )
    assert res == mutual_entailment


def test109():
    res, rs1, rs2, common = entailment(
        "Gli archeologi hanno timore di sbagliare i calcoli",
        "Gli archeologi temono di sbagliare i calcoli",
    )
    assert res == mutual_entailment


def test110():
    res, rs1, rs2, common = entailment("Mario ha mentito", "Mario ha detto una bugia")
    assert res == mutual_entailment


def test111():
    res, rs1, rs2, common = entailment("Il film ha impaurito Mario", "Mario ha paura")
    assert res == first_entails_second


def test112():
    res, rs1, rs2, common = entailment("Mario si propone", "Mario fa un'avance")
    assert res == first_entails_second


def test113():
    res, rs1, rs2, common = entailment(
        "Mario prende Luca a bacchettate", "Mario dà una bacchettata a Luca"
    )
    assert res == mutual_entailment


def test114():
    res, rs1, rs2, common = entailment(
        "La maestra spera", "La maestra nutre delle speranze"
    )
    assert res == mutual_entailment


def test115():
    res, rs1, rs2, common = entailment(
        "La maestra spera", "La maestra nutre delle speranze"
    )
    assert res == mutual_entailment


def test116():
    res, rs1, rs2, common = entailment(
        "Quel politico ha fatto degli errori", "Quel politico ha fatto una minchiata"
    )
    assert res == mutual_entailment


def test117():
    res, rs1, rs2, common = entailment("Mario ha fatto un'azione", "Mario ha agito")
    assert res == mutual_entailment


def test118():
    res, rs1, rs2, common = entailment("Mario ha avuto una delusione", "Mario è deluso")
    assert res == mutual_entailment


def test119():
    res, rs1, rs2, common = entailment(
        "Mario diede incomodo a Piero", "Mario ha disturbato Piero"
    )
    assert res == mutual_entailment


def test120():
    res, rs1, rs2, common = entailment(
        "Ho fatto fare una passeggiata al cane",
        "Io ho fatto fare una passeggiata al cane",
    )
    assert res == mutual_entailment


def test121():
    res, rs1, rs2, common = entailment(
        "Tu hai dato nocumento a Gianni", "Tu nuoci a Gianni"
    )
    assert res == mutual_entailment


def test122():
    res, rs1, rs2, common = entailment(
        "Hai fatto rasare il pelo al suo cane", "Il pelo viene rasato al suo cane"
    )
    assert res == first_entails_second


def test123():
    res, rs1, rs2, common = entailment(
        "Sandro diede scacco a Mario", "Mario è stato battuto da Sandro"
    )
    assert res == mutual_entailment


def test124():
    res, rs1, rs2, common = entailment(
        "Marta ha fatto fare una risata ai bambini", "I bambini ridono"
    )
    assert res == first_entails_second


def test125():
    res, rs1, rs2, common = entailment(
        "Marta ha fatto fare una risata ai bambini", "Marta fa ridere"
    )
    assert res == first_entails_second


def test126():
    res, rs1, rs2, common = entailment(
        "Maria ha fatto un racconto a Luigi", "A Luigi è stata raccontata una storia"
    )
    assert res == in_common
    expected_common = [DativeSemRole("LUIGI", ["raccontare"])]
    for ec in expected_common:
        assert ec in common["list"]
    assert len(common["list"]) == len(expected_common)


def test127():
    res, rs1, rs2, common = entailment(
        "Maria ha raccontato una storia a Luigi", "Maria ha fatto un racconto a Luigi"
    )
    assert res == first_entails_second


def test128():
    res, rs1, rs2, common = entailment(
        "Questo cibo fa schifo a Piero", "Questo cibo disgusta Piero"
    )
    assert res == mutual_entailment


def test129():
    res, rs1, rs2, common = entailment("Ho un brivido", "Rabbrividisco")
    assert res == mutual_entailment


def test130():
    res, rs1, rs2, common = entailment(
        "Sandra ha fatto delle grida", "Sandra ha emesso delle grida"
    )
    assert res == mutual_entailment


def test131():
    res, rs1, rs2, common = entailment(
        "I ragazzi hanno fatto un agguato a Sandro",
        "I ragazzi hanno fatto un assalto a Sandro",
    )
    assert res == mutual_entailment


def test132():
    res, rs1, rs2, common = entailment(
        "Mario farà una soperchieria al capo", "Mario farà delle angherie al capo"
    )
    assert res == mutual_entailment


def test133():
    res, rs1, rs2, common = entailment(
        "Mario ha dato scandalo", "Mario ha scandalizzato"
    )
    assert res == mutual_entailment


def test134():
    res, rs1, rs2, common = entailment(
        "Mario ha ingaggiato una battaglia", "Mario ha dato battaglia"
    )
    assert res == mutual_entailment


def test135():
    res, rs1, rs2, common = entailment(
        "Mario ha fatto degli ammiccamenti al compagno", "Mario gli ammiccava"
    )
    assert res == in_common
    expected_common = [OrdinarySemRole("MARIO", ["ammiccare"], ACTV)]
    for ec in expected_common:
        assert ec in common["list"]
    assert len(common["list"]) == len(expected_common)


def test136():
    res, rs1, rs2, common = entailment(
        "Mario ha fatto una telefonata a Luca", "Mario telefona a Luca"
    )
    assert res == mutual_entailment


def test137():
    res, rs1, rs2, common = entailment("è sorto il sole", "Il sole è sorto")
    assert res == mutual_entailment


def test138():
    res, rs1, rs2, common = entailment(
        "La pecora ha belato", "La pecora ha fatto un belato"
    )
    assert res == mutual_entailment


def test139():
    res, rs1, rs2, common = entailment(
        "Marco ha detto una menzogna", "Marco ha detto una bugia"
    )
    assert res == mutual_entailment


def test140():
    res, rs1, rs2, common = entailment(
        "Marco ha dato il benvenuto a Luca", "Marco ha accolto Luca"
    )
    assert res == mutual_entailment


def test141():
    res, rs1, rs2, common = entailment(
        "La politica ha impoverito i cittadini", "I cittadini si sono impoveriti"
    )
    assert res == first_entails_second


def test142():
    res, rs1, rs2, common = entailment(
        "Mario ha proposto una novità a Sandro", "Mario ha fatto una proposta a Sandro"
    )
    assert res == first_entails_second


def test143():
    res, rs1, rs2, common = entailment("Mario fa pratica", "Mario si impratichisce")
    assert res == mutual_entailment


def test144():
    res, rs1, rs2, common = entailment(
        "Mario ha fatto un'offesa a Luca", "Mario ha rivolto delle ingiurie a Luca"
    )
    assert res == mutual_entailment


def test145():
    res, rs1, rs2, common = entailment(
        "La luna ha eclissato il sole", "Il sole si è eclissato"
    )
    assert res == first_entails_second


def test146():
    res, rs1, rs2, common = entailment(
        "Il presidente ha rassegnato le proprie dimissioni",
        "Il presidente si è dimesso",
    )
    assert res == mutual_entailment


def test147():
    res, rs1, rs2, common = entailment("Mario ha paura", "Mario ha fifa")
    assert res == mutual_entailment


def test148():
    res, rs1, rs2, common = entailment(
        "Noi diamo il nostro appoggio a questo candidato",
        "Noi sosteniamo questo candidato",
    )
    assert res == mutual_entailment


def test149():
    res, rs1, rs2, common = entailment(
        "Queste letture infervorano Gianni", "Gianni si infervora"
    )
    assert res == first_entails_second


def test150():
    res, rs1, rs2, common = entailment("Gianni si infervora", "Gianni prende fervore")
    assert res == mutual_entailment


def test151():
    res, rs1, rs2, common = entailment("Gianni prova imbarazzo", "Gianni è imbarazzato")
    assert res == mutual_entailment


def test152():
    res, rs1, rs2, common = entailment(
        "L'oratore ha eccitato le folle", "Le folle si sono eccitate"
    )
    assert res == first_entails_second


def test153():
    res, rs1, rs2, common = entailment(
        "Piero ha dato dei regali ai bambini", "Dei regali furono dati ai bambini"
    )
    assert res == first_entails_second


def test154():
    res, rs1, rs2, common = entailment(
        "Piero ha dato dei regali ai bambini", "Furono dati dei regali ai bambini"
    )
    assert res == first_entails_second


def test155():
    res, rs1, rs2, common = entailment(
        "Mario ha pignorato la casa a Luca",
        "Mario fece un terribile pignoramento a Luca",
    )
    assert res == first_entails_second


def test156():
    res, rs1, rs2, common = entailment("Piero contrae una malattia", "Piero si ammala")
    assert res == mutual_entailment


def test157():
    res, rs1, rs2, common = entailment(
        "Mario ha preso un sorso d'acqua", "Mario ha bevuto"
    )
    assert res == first_entails_second


def test158():
    res, rs1, rs2, common = entailment(
        "Il nostro amico ha preso congedo", "Il nostro amico ha preso commiato"
    )
    assert res == mutual_entailment


def test159():
    res, rs1, rs2, common = entailment(
        "Il nostro amico ha opposto un netto rifiuto", "Il nostro amico ha rifiutato"
    )
    assert res == mutual_entailment


def test160():
    res, rs1, rs2, common = entailment(
        "Il razzismo procura solo un gran danno all'Italia",
        "Il razzismo danneggia l'Italia",
    )
    assert res == mutual_entailment


def test161():
    res, rs1, rs2, common = entailment(
        "Sandro ha mollato un ceffone a Luca", "Sandro ha schiaffeggiato Luca"
    )
    assert res == mutual_entailment


def test162():
    res, rs1, rs2, common = entailment(
        "Sandro ha mollato un ceffone a Luca", "Sandro ha allungato uno schiaffo a Luca"
    )
    assert res == mutual_entailment


def test163():
    res, rs1, rs2, common = entailment(
        "Mario ha consegnato il libro alla bibliotecaria", "Il libro è stato consegnato"
    )
    assert res == first_entails_second


def test164():
    res, rs1, rs2, common = entailment(
        "Mario ha consegnato il libro alla bibliotecaria",
        "Il libro è stato consegnato da Mario",
    )
    assert res == first_entails_second


def test165():
    res, rs1, rs2, common = entailment(
        "Mario ha consegnato il libro alla bibliotecaria",
        "Il libro è stato consegnato da Mario alla bibliotecaria",
    )
    assert res == mutual_entailment


def test166():
    res, rs1, rs2, common = entailment("Sandro ha un'intuizione", "Sandro ha intuito")
    assert res == mutual_entailment


def test167():
    res, rs1, rs2, common = entailment(
        "Mario ha mosso un addebito al cliente", "Mario ha fatto un addebito al cliente"
    )
    assert res == mutual_entailment


def test168():
    res, rs1, rs2, common = entailment(
        "Il libro è caduto", "Il libro ha fatto un tonfo"
    )
    assert res == second_entails_first


def test169():
    res, rs1, rs2, common = entailment(
        "Mario ha sferrato un colpo a Giorgio", "Giorgio è stato colpito da Mario"
    )
    assert res == mutual_entailment


def test170():
    res, rs1, rs2, common = entailment(
        "Mario ha fatto un pistolotto a Gianni", "Mario ha rimproverato Gianni"
    )
    assert res == first_entails_second


def test171():
    res, rs1, rs2, common = entailment(
        "Il padrone ha dato ascolto agli impiegati", "Il padrone ascolta gli impiegati"
    )
    assert res == mutual_entailment


def test172():
    res, rs1, rs2, common = entailment(
        "Mario ha allagato la casa", "La casa si è allagata"
    )
    assert res == first_entails_second


def test173():
    res, rs1, rs2, common = entailment(
        "Mario ha fatto mettere Aldo in imbarazzo da Giacomo", "Giacomo imbarazza Aldo"
    )
    assert res == first_entails_second


def test174():
    res, rs1, rs2, common = entailment(
        "Mario ha fatto mettere Aldo in imbarazzo da Giacomo",
        "Aldo è imbarazzato da Giacomo",
    )
    assert res == first_entails_second


def test175():
    res, rs1, rs2, common = entailment(
        "Mario ha fatto mettere Aldo in imbarazzo da Giacomo", "Aldo si è imbarazzato"
    )
    assert res == first_entails_second


def test176():
    res, rs1, rs2, common = entailment(
        "Mario ha fatto mettere Aldo in imbarazzo da Giacomo",
        "Giacomo mette in imbarazzo Aldo",
    )
    assert res == first_entails_second


def test177():
    res, rs1, rs2, common = entailment("Mario si guarisce", "Mario guarisce")
    assert res == first_entails_second


def test178():
    res, rs1, rs2, common = entailment("Mario si è guarito", "Mario è guarito")
    assert res == first_entails_second


def test179():
    res, rs1, rs2, common = entailment(
        "Mario ha preso un abbaglio", "Mario ha pigliato una cantonata"
    )
    assert res == mutual_entailment


def test180():
    res, rs1, rs2, common = entailment(
        "Quel generale combatte infinite guerre", "Si combattono infinite guerre"
    )
    assert res == first_entails_second


def test181():
    res, rs1, rs2, common = entailment("Il gatto infastidisce", "Il gatto dà fastidio")
    assert res == mutual_entailment


def test181_():
    res, rs1, rs2, common = entailment("Ha parlato a me", "Mi ha parlato")
    assert res == mutual_entailment


def test182():
    res, rs1, rs2, common = entailment(
        "Ha messo la scuola sotto sorveglianza", "La scuola è sorvegliata"
    )
    assert res == first_entails_second


def test183():
    res, rs1, rs2, common = entailment(
        "Mario ha fatto bisticciare gli amici", "Gli amici bisticciano"
    )
    assert res == first_entails_second


def test184():
    res, rs1, rs2, common = entailment(
        "Il ragazzo ha fatto una cazziata a Luca", "Il ragazzo ha rimproverato Luca"
    )
    assert res == mutual_entailment


def test185():
    res, rs1, rs2, common = entailment(
        "Mario ha proposto qualcosa a Sandro", "Qualcosa è stato proposto"
    )
    assert res == first_entails_second


def test186():
    res, rs1, rs2, common = entailment(
        "Mario ha proposto qualcosa a Sandro", "Qualcosa è stato proposto a Sandro"
    )
    assert res == first_entails_second


def test187():
    res, rs1, rs2, common = entailment("Io faccio jogging", "Io corro")
    assert res == first_entails_second


def test188():
    res, rs1, rs2, common = entailment(
        "Leo ha fatto una comparazione", "Leo ha fatto un paragone"
    )
    assert res == mutual_entailment


def test189():
    res, rs1, rs2, common = entailment(
        "I ragazzi hanno fatto cilecca", "I ragazzi hanno fallito"
    )
    assert res == mutual_entailment


def test190():
    res, rs1, rs2, common = entailment(
        "Questi problemi destano una forte preoccupazione",
        "Questi problemi suscitano preoccupazione",
    )
    assert res == mutual_entailment


def test191():
    res, rs1, rs2, common = entailment(
        "I ragazzi hanno fatto scomparire ogni traccia",
        "Ogni traccia è stata fatta scomparire dai ragazzi",
    )
    assert res == mutual_entailment


def test192():
    res, rs1, rs2, common = entailment("Mario allena Giulio", "Giulio si allena")
    assert res == first_entails_second


def test193():
    res, rs1, rs2, common = entailment(
        "Il capitano ha fatto affondare la nave", "Il capitano affonda la nave"
    )
    assert res == mutual_entailment


def test194():
    res, rs1, rs2, common = entailment(
        "Il capitano ha fatto affondare la nave", "Affonda la nave"
    )
    assert res == first_entails_second


def test195():
    res, rs1, rs2, common = entailment(
        "Il capitano ha fatto affondare la nave", "La nave affonda"
    )
    assert res == first_entails_second


def test196():
    res, rs1, rs2, common = entailment("Il capitano affonda la nave", "La nave affonda")
    assert res == first_entails_second


def test197():
    res, rs1, rs2, common = entailment("Il capitano affonda la nave", "Affonda la nave")
    assert res == first_entails_second


def test198():
    res, rs1, rs2, common = entailment("Ci vuole una dormita", "Serve una dormita")
    assert res == mutual_entailment


def test199():
    res, rs1, rs2, common = entailment(
        "Piero si è infatuato di Maria", "Piero ha una cotta per Maria"
    )
    assert res == mutual_entailment


def test200():
    res, rs1, rs2, common = entailment(
        "Piero prova una grande empatia", "Piero empatizza"
    )
    assert res == mutual_entailment


def test201():
    res, rs1, rs2, common = entailment(
        "Mario ha dispiaciuto Luigi", "Luigi si è dispiaciuto"
    )
    assert res == first_entails_second


def test202():
    res, rs1, rs2, common = entailment(
        "Piero mette in soggezione Mario", "Piero intimidisce Mario"
    )
    assert res == mutual_entailment


def test203():
    res, rs1, rs2, common = entailment(
        "Piero mette in soggezione Mario", "Mario è intimidito da Piero"
    )
    assert res == mutual_entailment


def test204():
    res, rs1, rs2, common = entailment(
        "Mario è messo in soggezione da Piero", "Mario è intimidito da Piero"
    )
    assert res == mutual_entailment


def test205():
    res, rs1, rs2, common = entailment(
        "Piero mette soggezione a Mario", "Mario è intimidito da Piero"
    )
    assert res == mutual_entailment


def test206():
    res, rs1, rs2, common = entailment(
        "Piero mette soggezione a Mario", "Mario è intimidito"
    )
    assert res == first_entails_second


def test207():
    res, rs1, rs2, common = entailment(
        "Luca ha fatto mettere in soggezione Mario da Piero",
        "Piero ha intimidito Mario",
    )
    assert res == first_entails_second


def test208():
    res, rs1, rs2, common = entailment(
        "Luca ha fatto mettere in soggezione Mario da Piero", "Mario si è intimidito"
    )
    assert res == first_entails_second


def test209():
    res, rs1, rs2, common = entailment(
        "Piero mette Luca in soggezione", "Piero mette soggezione a Luca"
    )
    assert res == mutual_entailment


def test210():
    res, rs1, rs2, common = entailment(
        "Mario ha messo sotto accusa Luca", "Mario ha fatto un'accusa a Luca"
    )
    assert res == mutual_entailment


def test211():
    res, rs1, rs2, common = entailment(
        "Luca fu messo in soggezione da Max", "Luca si è intimidito"
    )
    assert res == first_entails_second


def test212():
    res, rs1, rs2, common = entailment(
        "Mario ha fatto uno squillo a Luca", "Mario ha telefonato a Luca"
    )
    assert res == mutual_entailment


def test213():
    res, rs1, rs2, common = entailment(
        "Uno squillo fu fatto da Mario a Luca", "Mario ha telefonato a Luca"
    )
    assert res == mutual_entailment


def test214():
    res, rs1, rs2, common = entailment(
        "Mario mette in ambasce Luca", "Mario preoccupa Luca"
    )
    assert res == mutual_entailment


def test215():
    res, rs1, rs2, common = entailment(
        "Luca è messo in ambasce da Mario", "Mario preoccupa Luca"
    )
    assert res == mutual_entailment


def test216():
    res, rs1, rs2, common = entailment(
        "Mario ha messo il broncio", "Mario si è imbronciato"
    )
    assert res == mutual_entailment


def test217():
    res, rs1, rs2, common = entailment(
        "Mario ha visto te", "Tu sei stato visto da Mario"
    )
    assert res == mutual_entailment


def test218():
    res, rs1, rs2, common = entailment("Noi facciamo ginnastica", "Noi ci alleniamo")
    assert res == mutual_entailment


def test219():
    res, rs1, rs2, common = entailment("Facciamo ginnastica", "Ci alleniamo")
    assert res == mutual_entailment


def test220():
    res, rs1, rs2, common = entailment("Mario mi vede", "Mario vede me")
    assert res == mutual_entailment


def test221():
    res, rs1, rs2, common = entailment(
        "Mario ha donato qualcosa a Luigi", "Mario ha fatto un presente a Luigi"
    )
    assert res == first_entails_second


def test222():
    res, rs1, rs2, common = entailment(
        "La cosa ha avuto delle ripercussioni", "La cosa si è ripercossa"
    )
    assert res == mutual_entailment


def test223():
    res, rs1, rs2, common = entailment(
        "La cosa ha dato sollievo a Gianni", "La cosa ha rincuorato Gianni"
    )
    assert res == mutual_entailment


def test224():
    res, rs1, rs2, common = entailment(
        "Il padrone di casa ha sloggiato Mario", "Mario ha sloggiato"
    )
    assert res == first_entails_second


def test225():
    res, rs1, rs2, common = entailment(
        "La moglie aveva mentito al commissario",
        "La moglie ha detto una menzogna al commissario",
    )
    assert res == mutual_entailment


def test226():
    res, rs1, rs2, common = entailment("Ha mentito lui", "Lui ha detto una bugia")
    assert res == mutual_entailment


def test227():
    res, rs1, rs2, common = entailment(
        "Il presidente ha inasprito il conflitto", "Il conflitto si è inasprito"
    )
    assert res == first_entails_second


def test228():
    res, rs1, rs2, common = entailment(
        "Luigi fu fatto arrabbiare da Aldo", "Aldo fece arrabbiare Luigi"
    )
    assert res == mutual_entailment


def test229():
    res, rs1, rs2, common = entailment(
        "Maria ha accelerato il passo", "Maria ha accelerato"
    )
    assert res == first_entails_second


def test230():
    res, rs1, rs2, common = entailment(
        "Ci vuole un'intelligenza diabolica", "Serve un'intelligenza diabolica"
    )
    assert res == mutual_entailment


def test231():
    res, rs1, rs2, common = entailment(
        "IL suo comportamento ha insospettito Luca", "Luca si è insospettito"
    )
    assert res == first_entails_second


def test232():
    res, rs1, rs2, common = entailment("Mario ripone fiducia", "Mario si fida")
    assert res == mutual_entailment


def test233():
    res, rs1, rs2, common = entailment(
        "Mario ha fatto molta baldoria", "Mario si è divertito"
    )
    assert res == first_entails_second


def test234():
    res, rs1, rs2, common = entailment(
        "IL sole ha sbiadito la copertina", "La copertina si è sbiadita"
    )
    assert res == first_entails_second


def test235():
    res, rs1, rs2, common = entailment(
        "IL sole ha sbiadito la copertina", "La copertina è sbiadita"
    )
    assert res == first_entails_second


def test236():
    res, rs1, rs2, common = entailment(
        "La copertina si è sbiadita", "La copertina è sbiadita"
    )
    assert res == mutual_entailment


def test237():
    res, rs1, rs2, common = entailment(
        "Ho visto 4 simpatici amici", "Ho visto quattro simpatici amici"
    )
    assert res == mutual_entailment


def test238():
    res, rs1, rs2, common = entailment(
        "Luigi ha messo sotto accusa Giorgio", "Giorgio è sotto accusa"
    )
    assert res == first_entails_second


def test239():
    res, rs1, rs2, common = entailment("Giorgio è accusato", "Giorgio è sotto accusa")
    assert res == mutual_entailment


def test240():
    res, rs1, rs2, common = entailment(
        "Luigi ha messo sotto accusa Giorgio", "Giorgio è accusato"
    )
    assert res == first_entails_second


def test241():
    res, rs1, rs2, common = entailment(
        "Luigi ha messo sotto sorveglianza Giorgio", "Giorgio è sorvegliato"
    )
    assert res == first_entails_second


def test242():
    res, rs1, rs2, common = entailment(
        "Maria ha solleticato Aldo", "Maria ha fatto il solletico ad Aldo"
    )
    assert res == mutual_entailment


def test243():
    res, rs1, rs2, common = entailment(
        "Leo ha messo fuori gioco Piero", "Leo ha messo Piero fuori gioco"
    )
    assert res == mutual_entailment


def test244():
    res, rs1, rs2, common = entailment(
        "I senatori presero Cesare a pugnalate",
        "I senatori diedero delle pugnalate a Cesare",
    )
    assert res == mutual_entailment


def test245():
    res, rs1, rs2, common = entailment(
        "I senatori pugnalarono Cesare", "I senatori diedero delle pugnalate a Cesare"
    )
    assert res == mutual_entailment


def test246():
    res, rs1, rs2, common = entailment(
        "Qualcuno fece pugnalare Cesare dai senatori",
        "I senatori diedero delle pugnalate a Cesare",
    )
    assert res == first_entails_second


def test247():
    res, rs1, rs2, common = entailment(
        "Qualcuno fece pugnalare Cesare dai senatori", "I senatori pugnalarono Cesare"
    )
    assert res == first_entails_second


def test248():
    res, rs1, rs2, common = entailment(
        "Qualcuno fece pugnalare Cesare dai senatori",
        "Cesare è stato pugnalato dai senatori",
    )
    assert res == first_entails_second


def test249():
    res, rs1, rs2, common = entailment(
        "Mario ha preso una brutta scivolata", "Mario è scivolato"
    )
    assert res == mutual_entailment


def test250():
    couples = (
        ("ti", "te"),
        ("lo", "lui"),
        ("la", "lei"),
        ("vi", "voi"),
    )
    for couple in couples:
        a, b = couple
        f1 = f"Io {a} vedo"
        f2 = f"Io vedo {b}"
        res, rs1, rs2, common = entailment(f1, f2)
        assert res == mutual_entailment


def test251():
    sentences = {
        "Io ho mangiato la pasta",
        "Io mangio la pasta",
        "La pasta è mangiata da me",
        "Io mangiai la pasta",
        "La pasta fu mangiata da me",
    }
    entail_each_other(sentences)


def test252():
    group1 = {"Luigi ha fatto lavorare Antonio", "Luigi fece lavorare Antonio"}
    group2 = {"Antonio lavora", "Antonio ha lavorato", "Antonio lavorerà"}
    one_way_entailment(group1, group2)


def test253():
    couples = (("mi", "me"), ("lo", "lui"), ("la", "lei"))
    for couple in couples:
        a, b = couple
        f1 = f"Tu {a} vedi"
        f2 = f"Tu vedi {b}"
        res, rs1, rs2, common = entailment(f1, f2)
        assert res == mutual_entailment


def test254():
    res, rs1, rs2, common = entailment(
        "La guerra ha ingentilito Ungaretti", "Ungaretti si è ingentilito"
    )
    assert res == first_entails_second


def test255():
    group1 = {
        "Mario rasserena Piero",
        "Piero è rasserenato da Mario",
        "Mario infonde serenità a Piero",
    }
    group2 = {"Piero si rasserena", "Mario rasserena"}
    entail_each_other(group1)
    one_way_entailment(group1, group2)


def test256():
    g1 = set()
    for syn in {"truppe", "milizie"}:
        tmp = {
            f"Le {syn} hanno fatto un assedio alla città",
            f"L'assedio fu fatto alla città dalle {syn}",
            f"L'assedio fu fatto dalle {syn} alla città",
            f"L'assedio alla città fu fatto dalle {syn}",
            f"Le {syn} hanno messo la città sotto assedio",
            f"La città è stata messa sotto assedio dalle {syn}",
            f"Le {syn} hanno assediato la città",
            f"La città è stata assediata dalle {syn}",
        }
        g1 = g1.union(tmp)
    g2 = {"La città è sotto assedio", "La città è stata messa sotto assedio"}

    entail_each_other(g1)
    one_way_entailment(g1, g2, just_one=True)


def test257():
    res, rs1, rs2, common = entailment(
        "La mamma ha dato un calcio alla sedia", "La mamma ha preso a calci la sedia"
    )
    assert res == mutual_entailment


def test258():
    res, rs1, rs2, common = entailment(
        "Un calcio fu dato dalla mamma alla sedia",
        "La sedia fu presa a calci dalla mamma",
    )
    assert res == mutual_entailment


def test259():
    sentences = {
        "Max ha accoltellato Piero",
        "Piero è stato accoltellato da Max",
        "Max ha dato una coltellata a Piero",
        "Max ha tirato una coltellata a Piero",
        "Max ha inferto una coltellata a Piero",
        "Max ha tirato delle coltellate a Piero",
        "Una coltellata fu inferta a Piero da Max",
        "Una coltellata fu tirata a Piero da Max",
        "Una coltellata fu data a Piero da Max",
        "Una coltellata fu inferta da Max a Piero",
        "La coltellata fu data a Piero da Max",
        "Max ha preso Piero a coltellate",
        "Max ha preso a coltellate Piero",
        "Piero è stato preso a coltellate da Max",
        "Piero fu preso a coltellate da Max",
    }
    entail_each_other(sentences)


def test260():
    res, rs1, rs2, common = entailment(
        "Leo ha preso una sbandata per Anna", "Leo si è infatuato di Anna"
    )
    assert res == mutual_entailment


def test261():
    sentences = {
        "Il toro ha incornato il torero",
        "Il torero è stato incornato dal toro",
        "Il toro ha dato una cornata al torero",
        "Il toro ha tirato una cornata al torero",
        "Il toro ha inferto una cornata al torero",
        "Il toro ha tirato delle cornate al torero",
        "Il toro ha tirato cornate al torero",
        "Una cornata fu inferta al torero dal toro",
        "Una cornata fu tirata al torero dal toro",
        "Una cornata fu data al torero dal toro",
        "Una cornata fu inferta dal toro al torero",
        "Una cornata è stata inferta dal toro al torero",
        "Una cornata è stata inferta al torero dal toro",
        "Una cornata al torero è stata inferta dal toro",
        "Una cornata al torero è stata data dal toro",
        "La cornata fu data al torero dal toro",
        "Il toro ha preso il torero a cornate",
        "Il toro ha preso a cornate il torero",
        "Il torero è stato preso a cornate dal toro",
        "Il torero fu preso a cornate dal toro",
    }  # 20 frasi
    entail_each_other(sentences)


def test262():
    sentences = {
        "Max ha frustato Piero",
        "Piero è stato frustato da Max",
        "Max ha dato una frustata a Piero",
        "Max ha tirato una frustata a Piero",
        "Max ha inferto una frustata a Piero",
        "Max ha tirato delle frustate a Piero",
        "Una frustata fu inferta a Piero da Max",
        "Una frustata fu tirata a Piero da Max",
        "Una frustata fu data a Piero da Max",
        "Una frustata fu inferta da Max a Piero",
        "La frustata fu data a Piero da Max",
        "Max ha preso Piero a frustate",
        "Max ha preso a frustate Piero",
        "Piero è stato preso a frustate da Max",
        "Piero fu preso a frustate da Max",
    }
    entail_each_other(sentences)


def test263():
    sentences = {
        "Max ha manganellato Piero",
        "Piero è stato manganellato da Max",
        "Max ha dato una manganellata a Piero",
        "Max ha sferrato una manganellata a Piero",
        "Max ha inferto una manganellata a Piero",
        "Max ha sferrato delle manganellate a Piero",
        "Una manganellata fu inferta a Piero da Max",
        "Una manganellata fu sferrata a Piero da Max",
        "Una manganellata fu data a Piero da Max",
        "Una manganellata fu inferta da Max a Piero",
        "La manganellata fu data a Piero da Max",
        "Max ha preso Piero a manganellate",
        "Max ha preso a manganellate Piero",
        "Piero è stato preso a manganellate da Max",
        "Piero fu preso a manganellate da Max",
    }
    entail_each_other(sentences)


def test264():
    sentences = {
        "Il cane ha morso il gatto",
        "Il cane morde il gatto",
        "Il gatto è stato morso dal cane",
        "Il cane ha dato un morso al gatto",
        "Il cane ha dato dei morsi al gatto",
        "Un morso fu dato al gatto dal cane",
        "Il morso fu dato dal cane al gatto",
        "Il cane ha preso il gatto a morsi",
        "Il cane ha preso a morsi il gatto",
        "Il gatto è stato preso a morsi dal cane",
        "Il gatto fu preso a morsi dal cane",
    }
    entail_each_other(sentences)


def test265():
    res, rs1, rs2, common = entailment(
        "Loro hanno fatto pace", "Loro si sono rappacificati"
    )
    assert res == mutual_entailment


def test266():
    res, rs1, rs2, common = entailment(
        "Il dialogo ha rappacificato i ragazzi", "I ragazzi si sono rappacificati"
    )
    assert res == first_entails_second


def test267():
    sentences = {
        "Il film ha messo spavento ai ragazzi",
        "Il film ha spaventato i ragazzi",
        "I ragazzi furono spaventati dal film",
    }
    entail_each_other(sentences)


def test268():
    res, rs1, rs2, common = entailment(
        "Il film ha messo spavento ai ragazzi", "I ragazzi si sono spaventati"
    )
    assert res == first_entails_second


def test269():
    sentences = {
        "Piero ha dato una pedata al cane",
        "Piero ha preso a pedate il cane",
        "Piero ha preso il cane a pedate",
        "Le pedate sono state date al cane da Piero",
        "Il cane è stato preso a pedate da Piero",
    }
    entail_each_other(sentences)


def test270():
    res, rs1, rs2, common = entailment(
        "Piero ha preso a spintoni Luca", "Piero ha spinto Luca"
    )
    assert res == mutual_entailment


def test271():
    group1 = {
        "Mario ha fatto sorridere Luigi",
        "Mario ha fatto fare un sorriso a Luigi",
    }
    group2 = {"Mario ha fatto sorridere", "Luigi sorride", "Luigi sorriderà"}
    entail_each_other(group1)
    one_way_entailment(group1, group2)


def test272():
    res, rs1, rs2, common = entailment(
        "Mario fa l'occhiolino a Giulia", "Mario ammicca a Giulia"
    )
    assert res == mutual_entailment


def test273():
    group1 = {
        "Mario fa l'occhiolino a Giulia",
        "Mario fa un ammiccamento a Giulia",
        "Mario ammicca a Giulia",
    }
    group2 = {"Mario fa l'occhiolino", "Mario fa un ammiccamento", "Mario ammicca"}
    entail_each_other(group1)
    one_way_entailment(group1, group2)


def test274():
    res, rs1, rs2, common = entailment(
        "Loro hanno fatto bisboccia", "Loro hanno fatto baldoria"
    )
    assert res == in_common
    expected_common = [OrdinarySemRole("LORO", ["DIVERTIRE"], "ACTIVE_SI")]
    for ec in expected_common:
        assert ec in common["list"]
    assert len(common["list"]) == len(expected_common)


def test275():
    res, rs1, rs2, common = entailment(
        "Loro hanno fatto il tutto", "Il tutto è stato fatto da loro"
    )
    assert res == mutual_entailment


def test277():
    sentences = {
        "Max ha dato una scorsa al libro",
        "Max ha dato un'occhiata al libro",
        "Max ha dato una guardata al libro",
        "Max ha dato una guardatina al libro",
        "Una guardatina fu data da Max al libro",
    }
    entail_each_other(sentences)


def test278():
    group1 = {"Leo ha dato una controllatina al progetto", "Leo controlla il progetto"}
    group2 = {"Leo fa un controllo", "Leo controlla", "Leo ha dato una controllatina"}
    entail_each_other(group1)
    one_way_entailment(group1, group2)


def test279():
    sentences = {
        "Leo ha dato consolazione a Pio'",
        "Pio è consolato da Leo",
        "Leo consola Pio",
    }
    entail_each_other(sentences)


def test280():
    group1 = {
        "Max ha messo Luca sotto accusa",
        "Max ha messo sotto accusa Luca",
        "Luca fu messo sotto accusa da Max",
        "Max ha accusato Luca",
        "Luca fu accusato da Max",
        "Max ha fatto un'accusa a Luca",
        "Un'accusa è stata fatta a Luca da Max",
    }
    group2 = {
        "Luca è sotto accusa",
        "Luca è accusato",
        "Max accusa",
        "Un'accusa è stata fatta a Luca",
        "Un'accusa è stata fatta da Max",
    }
    entail_each_other(group1)
    one_way_entailment(group1, group2)


def test281():
    res, rs1, rs2, common = entailment(
        "Luca ha fatto uno sfuriata", "Luca si è sfogato"
    )
    assert res == first_entails_second


def test282():
    sentences = {
        "Max ha bastonato Piero",
        "Piero è stato bastonato da Max",
        "Max ha dato una bastonata a Piero",
        "Max ha assestato una bastonata a Piero",
        "Max ha assestato una bastonata a Piero",
        "Max ha assestato delle bastonate a Piero",
        "Una bastonata fu assestata a Piero da Max",
        "Una bastonata fu assestata a Piero da Max",
        "Una bastonata fu data a Piero da Max",
        "Una bastonata fu assestata da Max a Piero",
        "La bastonata fu data a Piero da Max",
        "Max ha preso Piero a bastonate",
        "Max ha preso a bastonate Piero",
        "Piero è stato preso a bastonate da Max",
        "Piero fu preso a bastonate da Max",
    }
    entail_each_other(sentences)


def test283():
    sentences = {
        "Max ha sculacciato Piero",
        "Piero è stato sculacciato da Max",
        "Max ha dato una sculacciata a Piero",
        "Max ha mollato una sculacciata a Piero",
        "Max ha mollato una sculacciata a Piero",
        "Max ha mollato delle sculacciate a Piero",
        "Una sculacciata fu mollato a Piero da Max",
        "Una sculacciata fu mollato a Piero da Max",
        "Una sculacciata fu data a Piero da Max",
        "Una sculacciata fu inferta da Max a Piero",
        "La sculacciata fu data a Piero da Max",
        "Max ha preso Piero a sculacciate",
        "Max ha preso a sculacciate Piero",
        "Piero è stato preso a sculacciate da Max",
        "Piero fu preso a sculacciate da Max",
    }
    entail_each_other(sentences)


def test284():
    sentences = {"Max ha fatto una stirata", "Max ha fatto una stiratina"}
    entail_each_other(sentences)


def test285():
    group1 = {
        "Max ha fatto una strage",
        "Max ha fatto un eccidio",
        "Un eccidio è stato fatto da Max",
    }
    group2 = {"Max ha ucciso", "Un eccidio è stato fatto", "Una strage è stato fatta"}
    entail_each_other(group1)
    one_way_entailment(group1, group2)


def test286():
    group1 = {
        "Max mette Luca nella merda",
        "Max mette Luca nei guai",
        "Max inguaia Luca",
    }
    group2 = {"Luca è nei guai", "Luca è nella merda", "Luca è inguaiato"}
    entail_each_other(group1)
    one_way_entailment(group1, group2)


def test287():
    group1 = {"Mario ha iniziato la festa"}
    group2 = {"La festa è iniziata"}
    one_way_entailment(group1, group2)


def test288():
    group1 = {"Max si è fatto prendere a schiaffi da Luigi"}
    group2 = {
        "Max è stato schiaffeggiato",
        "Max è preso a schiaffi",
        "Si schiaffeggia Max",
        "Luigi ha preso a schiaffi Max",
        "Luigi schiaffeggia Max",
    }
    entail_each_other(group1)
    one_way_entailment(group1, group2)


def test289():  # it tests the synonymy between 'sganassoni and 'ceffoni' (based on strings rather than lemmas)
    sentences = {
        "L'autista ha preso a sganassoni Mario",
        "L'autista ha preso Mario a ceffoni",
        "L'autista ha preso Mario a scapaccioni",
        "L'autista ha preso Mario a sberle",
        "L'autista ha preso Mario a manrovesci",
    }
    entail_each_other(sentences)


def test290():
    res, rs1, rs2, common = entailment(
        "Mario ha fatto un vero diktat a Luigi", "Mario impone qualcosa a Luigi"
    )
    assert res == in_common
    expected_common = [
        OrdinarySemRole("MARIO", ["IMPORRE"], ACTV),
        DativeSemRole("LUIGI", ["IMPORRE"]),
    ]
    for ec in expected_common:
        assert ec in common["list"]
    assert len(common["list"]) == len(expected_common)


def test291():
    group1 = {
        "Leo ha fatto delle coccole a Laura",
        "Le coccole sono state fatte da Leo a Laura",
        "Leo ha coccolato Laura",
        "Laura è stata coccolata da Leo",
    }
    group2 = {"Leo coccola", "Laura è coccolata", "Leo fa coccole"}
    entail_each_other(group1)
    one_way_entailment(group1, group2)


def test292():
    group1 = {
        "Leo ha dato coraggio a Luca",
        "Leo ha dato un incoraggiamento a Luca",
        "Leo ha incoraggiato Luca",
        "Luca è stato incoraggiato da Leo",
        "Un incoraggiamento fu dato da Leo a Luca",
    }
    group2 = {"Leo incoraggia", "Leo dà coraggio", "Luca è incoraggiato"}
    entail_each_other(group1)
    one_way_entailment(group1, group2)


def test293():
    res, rs1, rs2, common = entailment("Leo fa la pacchia", "Leo si diverte")
    assert res == first_entails_second


def test294():
    res, rs1, rs2, common = entailment("Leo fa la pacchia", "Mario diverte Leo")
    assert res == in_common
    expected_common = [OrdinarySemRole("LEO", ["DIVERTIRE"], ACTV_S)]
    for ec in expected_common:
        assert ec in common["list"]
    assert len(common["list"]) == len(expected_common)
    # attenzione: 'diverte' è anche 3a SG di 'divergere' (try 'Il film diverte Leo')


def test295():
    res, rs1, rs2, common = entailment(
        "Luca ha fatto un'escursione", "Luca ha fatto una gita"
    )
    assert res == mutual_entailment


def test296():
    group1 = {
        "Mario si è preso una sbornia",
        "Mario si è preso un'ubriacatura",
        "Mario ha preso una sbornia",
        "Mario si ubriaca",
    }
    entail_each_other(group1)


def test297():
    group1 = {
        "Questa musica infastidisce Luca",
        "Luca è infastidito da questa musica",
        "Questa musica dà noie a Luca",
    }
    group2 = {"Questa musica infastidisce", "Luca si infastidisce"}
    entail_each_other(group1)
    one_way_entailment(group1, group2)


def test298():
    group1 = {"Il gatto ha intrappolato il topo", "Il topo è intrappolato dal gatto"}
    group2 = {"Il topo è intrappolato"}
    entail_each_other(group1)
    one_way_entailment(group1, group2)


def test299():
    group1 = {"Il caldo dà fastidio a Sandra", "Il caldo infastidisce Sandra"}
    group2 = {"Il caldo infastidisce", "Sandra è infastidita"}
    entail_each_other(group1)
    one_way_entailment(group1, group2)


def test300():
    group1 = {
        "La battuta ha fatto sorridere gli spettatori",
        "Gli spettatori sono stati fatti sorridere dalla battuta",
    }
    group2 = {"Gli spettatori hanno sorriso", "Gli spettatori hanno fatto un sorriso"}
    entail_each_other(group1)
    one_way_entailment(group1, group2)


def test301():
    res, rs1, rs2, common = entailment(
        "Gli spettatori piangono",
        "Gli spettatori hanno fatto un pianto",
    )
    assert res == mutual_entailment


def test302():
    group1 = {
        "Maria ha sorriso a Piero",
        "Maria ha fatto un sorriso a Piero",
        "Un sorriso fu fatto a Piero da Maria",
    }
    group2 = {"Maria sorride", "Maria ha fatto un sorriso"}
    entail_each_other(group1)
    one_way_entailment(group1, group2)


def test303():
    group1 = {
        "L'avvocato fece accusare il tecnico da Mario",
        "L'avvocato fece mettere il tecnico sotto accusa da Mario",
    }
    group2 = {
        "Mario ha accusato il tecnico",
        "Il tecnico fu fatto accusare dall'avvocato",
        "Mario ha fatto un'accusa al tecnico",
        "Mario ha lanciato un'accusa al tecnico",
        "Mario ha rivolto un'accusa al tecnico",
        "Mario ha mosso un'accusa al tecnico",
        "Mario ha messo il tecnico sotto accusa",
    }
    entail_each_other(group1)
    one_way_entailment(group1, group2)


def test304():
    res, rs1, rs2, common = entailment(
        "Mario ha lanciato un'occhiataccia a Luca", "Mario guarda Luca"
    )
    assert res == first_entails_second


def test305():
    res, rs1, rs2, common = entailment(
        "Hai fatto una pernacchia a Sandro", "Hai preso a pernacchie Sandro"
    )
    assert res == mutual_entailment


def test306():
    res, rs1, rs2, common = entailment(
        "Mario ha dato vigore al progetto", "Mario ha rinvigorito il progetto"
    )
    assert res == mutual_entailment


def test307():
    res, rs1, rs2, common = entailment(
        "Mario ha fatto una sfacchinata", "Mario ha faticato"
    )
    assert res == first_entails_second


def test308():
    res, rs1, rs2, common = entailment("Mario pascola le pecore", "Le pecore pascolano")
    assert res == first_entails_second


def test309():
    res, rs1, rs2, common = entailment(
        "Mario ha preso Gianni a colpi di bacchetta",
        "Mario ha dato dei colpi di bacchetta a Gianni",
    )  # colpo = iperonimo
    assert res == first_entails_second


def test310():
    res, rs1, rs2, common = entailment(
        "Il testimone ha fatto chiarezza", "Il testimone ha dato un chiarimento"
    )
    assert res == mutual_entailment


def test311():
    res, rs1, rs2, common = entailment("Mario fa un selfie", "Mario si fotografa")
    assert res == second_entails_first


def test312():
    res, rs1, rs2, common = entailment(
        "La notizia ha avuto risonanza", "La notizia ha avuto risalto"
    )
    assert res == mutual_entailment


def test313():
    res, rs1, rs2, common = entailment(
        "Mario ha approfondito il caso", "Mario ha fatto un approfondimento"
    )
    assert res == first_entails_second


def test314():
    res, rs1, rs2, common = entailment(
        "Il vigile ha fatto una contravvenzione all'automobilista",
        "Il vigile ha multato l'automobilista",
    )
    assert res == mutual_entailment


def test315():
    res, rs1, rs2, common = entailment("Il cibo fa puzza", "Il cibo puzza")
    assert res == mutual_entailment


def test316():
    res, rs1, rs2, common = entailment(
        "Ho tirato un calcione a Luca", "Ho sferrato un calcio a Luca"
    )
    assert res == mutual_entailment


def test317():
    res, rs1, rs2, common = entailment("Mi ha preso a cinghiate", "Mi ha colpito")
    assert res == first_entails_second


def test318():
    res, rs1, rs2, common = entailment("Lui mi ha dato sostegno", "Mi ha aiutato")
    assert res is no_entailment


def test319():
    res, rs1, rs2, common = entailment("Lui mi ha dato sostegno", "Lui mi ha aiutato")
    assert res == second_entails_first


def test320():
    res, rs1, rs2, common = entailment("Mario prova disgusto", "Mario è disgustato")
    assert res == mutual_entailment


def test321():
    res, rs1, rs2, common = entailment("Lo chiami", "Chiami lui")
    assert res == mutual_entailment


def test322():
    res, rs1, rs2, common = entailment("Max cova la speranza", "Max nutre una speranza")
    assert res == mutual_entailment


def test323():
    res, rs1, rs2, common = entailment(
        "Max ha commesso una sgarberia", "Max ha fatto uno sgarbo"
    )
    assert res == mutual_entailment


def test324():
    res, rs1, rs2, common = entailment(
        "Mario ha fatto una prepotenza a Luigi", "Mario vessa Luigi"
    )
    assert res == mutual_entailment


def test325():
    res, rs1, rs2, common = entailment(
        "I bravi hanno teso un'imboscata al prete",
        "I bravi hanno fatto un agguato al prete",
    )
    assert res == mutual_entailment


def test326():
    res, rs1, rs2, common = entailment(
        "Mario ha preso una sbandata per Laura", "Mario ha preso una cotta per Laura"
    )
    assert res == mutual_entailment


def test327():
    group1 = {
        "Mario ha fatto una cavolata",
        "Mario ha fatto una cazzata",
        "Mario ha fatto una corbelleria",
        "Mario ha fatto un errore",
        "Mario ha fatto un errorino",
        "Mario ha fatto un erroraccio",
        "Mario ha fatto una gaffe",
        "Mario ha fatto delle gaffes",
        "Mario ha fatto una minchiata",
        "Mario ha fatto una scemenza",
        "Mario ha fatto una sciocchezza",
        "Mario ha fatto una stupidaggine",
        "Mario ha fatto una stupidata",
        "Mario ha fatto uno sbaglio",
        "Mario sbaglia",
    }
    entail_each_other(group1)


def test328():
    res, rs1, rs2, common = entailment(
        "Il film mette tristezza", "Il film fa tristezza"
    )
    assert res == mutual_entailment


def test329():
    res, rs1, rs2, common = entailment(
        "Ha dato una spallata a Piero", "Ha colpito Piero"
    )
    assert res == first_entails_second


def test330():
    res, rs1, rs2, common = entailment(
        "Maria ha dato un abbraccio alla zia", "Maria ha abbracciato la zia"
    )
    assert res == mutual_entailment


def test331():
    res, rs1, rs2, common = entailment(
        "Ci prendiamo a sberle", "Noi ci prendiamo a sberle"
    )
    assert res == mutual_entailment


def test332():
    res, rs1, rs2, common = entailment(
        "Luca fu messo in soggezione da Max", "Luca è in soggezione"
    )
    assert res == first_entails_second


def test333():
    res, rs1, rs2, common = entailment("Sandro prova invidia", "Sandro invidia Luigi")
    assert res == second_entails_first


def test334():
    group1 = {
        "Collaudo",
        "Io collaudo",
        "Io faccio un collaudo",
        "Faccio un collaudo",
    }
    entail_each_other(group1)


def test335():
    res, rs1, rs2, common = entailment(
        "Leo ci ha fatto spaventare", "Ci siamo spaventati"
    )
    assert res == first_entails_second


def test336():
    res, rs1, rs2, common = entailment("Piero è caduto", "Piero ha fatto un ruzzolone")
    assert res == second_entails_first


def test337():
    res, rs1, rs2, common = entailment(
        "Lea ha consegnato la posta a Sandra", "Lea le ha consegnato la posta"
    )
    assert True


def test338():
    res, rs1, rs2, common = entailment("Lea le ha parlato", "Lea ha parlato a lei")
    assert res == mutual_entailment


def test339():
    res, rs1, rs2, common = entailment("Lea le ha parlato", "Lea ha parlato a Sandra")
    assert True


def test340():
    res, rs1, rs2, common = entailment(
        "Mario mette in catene Luca", "MArio mette Luca alla catena"
    )
    assert res == mutual_entailment


def test341():
    res, rs1, rs2, common = entailment(
        "Piero è stato fatto cadere da Luigi", "Luigi ha fatto cadere Piero"
    )
    assert res == mutual_entailment


def test342():
    res, rs1, rs2, common = entailment(
        "Max ha dato una fregatura a Giorgio",
        "Max ha imbrogliato Giorgio",
    )
    assert res == mutual_entailment


def test343():
    res, rs1, rs2, common = entailment(
        "Loro hanno fatto una contestazione", "Loro hanno contestato"
    )
    assert res == mutual_entailment


def test344():
    res, rs1, rs2, common = entailment("Mario fa sognare me", "MArio mi fa sognare")
    assert res == mutual_entailment


def test345():
    res, rs1, rs2, common = entailment(
        "Mario ha fatto regalare un orologio a te",
        "Mario ti ha fatto regalare un orologio",
    )
    assert res == mutual_entailment
