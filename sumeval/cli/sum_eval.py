import json
import plac
from itertools import groupby
from statistics import mean
from sumeval.metrics.rouge import RougeCalculator


def main(
    score_desc: "ex: To calculate ROUGE-N, L, BE => 'r-nlb'",
    use_file: ("read data from file", "flag", "f"),
    include_stopwords: ("don't ignore stop words", "flag", "in"),
    stemming: ("use stemming", "flag", "st"),
    word_limit: ("word limit count", "option", "wl") = -1,
    length_limit: ("sentence limit length", "option", "ll") = -1,
    alpha: ("alpha for f1-score", "option") = 0.5,
    language: ("word limit count", "option", "la") = "en",
    *params):

    score_type, score_kinds = score_desc.lower().split("-")
    if len(params) < 2:
        print("You have to specify at least one summary and reference.")
        return

    summary = params[0]
    references = params[1:]
    stopwords = not include_stopwords

    scores = []
    if score_type == "r":
        scorer = RougeCalculator(
            stopwords=stopwords, stemming=stemming,
            word_limit=word_limit, length_limit=length_limit,
            lang=language)

        generator = None
        if use_file:
            generator = file_generator(summary, references)
        else:
            generator = sentence_to_generator(summary, references)

        keys = []
        for s, rs in generator:
            score = {}
            for k in score_kinds:
                if k == "n":
                    score["ROUGE-1"] = scorer.rouge_1(s, rs, alpha)
                    score["ROUGE-2"] = scorer.rouge_2(s, rs, alpha)
                elif k == "l":
                    score["ROUGE-L"] = scorer.rouge_l(s, rs, alpha)
                elif k == "b":
                    score["ROUGE-BE"] = scorer.rouge_be(s, rs, "HMR", alpha)
            if len(keys) == 0:
                keys = list(score.keys())
            scores.append(score)

    avgs = {}
    for k in keys:
        avg = mean([s[k] for s in scores])
        avgs[k] = avg

    result = {
        "options": {
            "stopwords": stopwords,
            "stemming": stemming,
            "word_limit": word_limit,
            "length_limit": length_limit,
            "alpha": alpha,
            "input-summary": summary,
            "input-references": references
        },
        "averages": avgs,
        "scores": scores
    }

    output = json.dumps(result, indent=2, ensure_ascii=False)
    print(output)


def file_generator(s_file_path, r_file_paths):
    s_file = open(s_file_path, encoding="utf-8")
    r_files = [open(r, encoding="utf-8") for r in r_file_paths]
    for lines in zip(s_file, *r_files):
        lines = [ln.strip() for ln in lines]
        yield lines[0], lines[1:]
    else:
        s_file.close()
        for r in r_files:
            r.close()


def sentence_to_generator(summary, references):
    yield summary, references


def entry_point():
    plac.call(main)


if __name__ == "__main__":
    entry_point()
