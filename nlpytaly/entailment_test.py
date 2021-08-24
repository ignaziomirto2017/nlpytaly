from nlpytaly import entailment
from nlpytaly.operations.semantic_roles.SemRole import OrdinarySemRole

first_entails_second = -1
mutual_entailment = 0
no_entailment = None
second_entails_first = 1
suppletive = 3
in_common = 4


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
        "Mario insulta l'amico", "Mario ha preso a parolacce l'amico",
    )
    assert res == second_entails_first


def test4():
    res, rs1, rs2, common = entailment(
        "Mario ha preso a cazzotti l'amico", "Mario ha colpito l'amico",
    )
    assert res == first_entails_second


def test5():
    res, rs1, rs2, common = entailment(
        "Mario ha preso a cazzotti l'amico", "Mario ha preso a pedate l'amico"
    )
    assert res is suppletive


def test6():
    res, rs1, rs2, common = entailment(
        "Mario ha fatto visitare il bambino dal medico", "Il medico visita il bambino"
    )
    assert res == first_entails_second


def test7():
    res, rs1, rs2, common = entailment(
        "Mario fa il meccanico", "Mario fa il poliziotto"
    )
    assert res == suppletive


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
        "L'amico prende a cazzotti Antonio", "L'amico prende a pugni Antonio",
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
        "Leonardo ha fatto arrabbiare l'amico", "L'amico si arrabbia",
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
        "L'uomo aggredito ha denunciato gli assalitori", "Si aggredì l'uomo",
    )
    assert res == first_entails_second


def test19():
    res, rs1, rs2, common = entailment(
        "Il professore prende la ragazza a pugni",
        "Il professore prende la ragazza a sassate",
    )
    assert res is suppletive


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
        "Mario ha fatto fare un sorriso a Giulia", "Giulia ha sorriso",
    )
    assert res == first_entails_second


def test32():
    res, rs1, rs2, common = entailment(
        "Mario ha fatto fare un sorriso a Giulia", "Mario ha fatto sorridere Giulia",
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
        OrdinarySemRole("LA NONNA", ["accompagnare"], "ACTIVE"),
        OrdinarySemRole("IL BAMBINO", ["accompagnare"], "PASSIVE"),
    ]
    for ec in expected_common:
        assert ec in common
    assert len(common) == len(expected_common)


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
    assert res == mutual_entailment


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


def test50():
    res, rs1, rs2, common = entailment(
        "Sandro ha preso a cazzotti Giulio", "Giulio è stato preso a legnate da Sandro",
    )
    assert res is suppletive


def test51():
    res, rs1, rs2, common = entailment(
        "Il meccanismo si è inceppato", "Il meccanismo è inceppato",
    )
    assert res == mutual_entailment


def test52():
    res, rs1, rs2, common = entailment(
        "La ruggine ha inceppato l'arma.", "L'arma si inceppa.",
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
        "Il comandante ha fatto mettere agli arresti il ladro dal sergente",
        "Il ladro è stato arrestato dal sergente",
    )
    assert res == first_entails_second


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
        "Mario ha fatto fare un sorriso a Giulia", "Mario ha fatto sorridere Giulia"
    )
    assert res == mutual_entailment


def test58():
    res, rs1, rs2, common = entailment(
        "Una task force ha fatto un'incursione in territorio sovietico",
        "Una task force penetra in territorio sovietico",
    )
    assert res == mutual_entailment


def test59():
    res, rs1, rs2, common = entailment(
        "Voi faceste arrestare l'uomo alla donna", "Faceste arrestare l'uomo alla donna"
    )
    assert res == mutual_entailment


def test60():
    res, rs1, rs2, common = entailment(
        "I ragazzi sono stati presi a bacchettate", "i ragazzi bacchettati",
    )
    assert res == first_entails_second


def test61():
    res, rs1, rs2, common = entailment(
        "Questa politica economia indebita lo Stato", "Lo stato si indebita",
    )
    assert res == first_entails_second


def test62():
    res, rs1, rs2, common = entailment(
        "Mario ha dato la cartellina alla sorella", "Mario dà la cartellina",
    )
    assert res == first_entails_second


def test63():
    res, rs1, rs2, common = entailment("Piero si è distratto", "Piero è distratto",)
    assert res == mutual_entailment


def test64():
    res, rs1, rs2, common = entailment(
        "Sandro ha distratto Piero", "Piero si è distratto",
    )
    assert res == first_entails_second


def test65():
    res, rs1, rs2, common = entailment(
        "Sandro ha distratto Piero", "Piero è distratto",
    )
    assert res == first_entails_second


def test66():
    res, rs1, rs2, common = entailment(
        "Sandro ha impietosito Piero", "Piero si è impietosito",
    )
    assert res == first_entails_second


def test67():
    res, rs1, rs2, common = entailment(
        "Marco inebetisce Luca", "Luca è stato inebetito da Marco",
    )
    assert res == mutual_entailment


def test68():
    res, rs1, rs2, common = entailment("Marco inebetisce Luca", "Luca si è inebetito",)
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
    assert res is suppletive


def test72():
    res, rs1, rs2, common = entailment(
        "Ho riempito la vasca", "La vasca si è riempita",
    )
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
        "Leonardo fece aprire la porta a Maria da Luca",
        "Leonardo fece aprire la porta",
    )
    assert res == first_entails_second


def test76():
    res, rs1, rs2, common = entailment(
        "Leonardo fece aprire la porta a Maria da Luca", "Leonardo fece aprire",
    )
    assert res == first_entails_second


def test77():
    res, rs1, rs2, common = entailment(
        "Leonardo si fece aprire la porta da Luca", "Leonardo fece aprire la porta",
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
        "L'autista ha fermato la macchina", "La macchina si è fermata",
    )
    assert res == first_entails_second


def test81():
    res, rs1, rs2, common = entailment(
        "La lezione ha fatto rincretinire gli studenti", "Gli studenti rincretiniscono",
    )
    assert res == first_entails_second


def test82():
    res, rs1, rs2, common = entailment(
        "La lezione ha rincretinito gli studenti", "Gli studenti rincretiniscono",
    )
    assert res == first_entails_second


def test83():
    res, rs1, rs2, common = entailment(
        "Mario ha corso un rischio", "Mario ha corso un pericolo",
    )
    assert res == mutual_entailment


def test84():
    res, rs1, rs2, common = entailment(
        "Piero ha confuso gli spettatori", "Gli spettatori sono confusi",
    )
    assert res == first_entails_second


def test85():
    res, rs1, rs2, common = entailment(
        "Sandro indispettisce i ragazzi", "I ragazzi sono indispettiti",
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
        "Piero ha dato i regali alle bambine", "Alle bambine furono dati i regali",
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
