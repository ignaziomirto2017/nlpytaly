from nlpytaly import nlpytaly


def tag(s: str):
    tagger = nlpytaly()
    result = tagger.tag(s)

    for k, v in result.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    tag("Gli abbiamo chiesto di fare un sorriso a Giulia")
