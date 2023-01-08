from nlpytaly import NLPYTALY, entailment


def tag(s: str):
    tagger = NLPYTALY()
    result = tagger.tag(s)

    for k, v in result.items():
        print(f"{k}: {v}")


def entailment_(s1, s2):
    res, _, _, common = entailment(s1, s2)
    if res is None:
        print(f"'{s1}' and '{s2}' do not entail each other")
    elif res == 0:
        print(f"'{s1}' and '{s2}' entail each other")
    elif res == -1:
        print(f"'{s1}' entails '{s2}'")
    elif res == 1:
        print(f"'{s2}' entails '{s1}'")
    elif res == 3:
        print(
            f"'{s1}' and '{s2}' do not entail each other. However, both of them yield the following semantic role(s):"
        )
        for tmp in common:
            print(" - ", tmp)


if __name__ == "__main__":
    # tag("Gli abbiamo chiesto di fare un sorriso a Giulia")
    entailment_(
        "Le maestre prendono a bacchettate i bambini",
        "I bambini sono presi a bacchettate",
    )
    entailment_("Mario ha mangiato la pasta", "Mario canta")
    entailment_("Mario insulta l'amico", "Mario ha preso a parolacce l'amico")
    entailment_("Mario ha preso a cazzotti l'amico", "Mario ha colpito l'amico")
    entailment_("Mario ha preso a cazzotti l'amico", "Mario ha preso a pedate l'amico")
    entailment_(
        "Mario ha fatto visitare il bambino dal medico", "Il medico visita il bambino"
    )
    entailment_("Mario fa il meccanico", "Mario fa il poliziotto")
    entailment_("Mario ha preso a cazzotti l'amico", "Mario ha preso a pugni l'amico")
    entailment_("Mario mangia la pasta", "La pasta è mangiata da Mario")
