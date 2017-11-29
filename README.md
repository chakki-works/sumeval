# sumeval

Well tested evaluation framework for text summarization.

The implementation is pure Python, and its 
scores are tested compare with [original Perl script (ROUGE-1.5.5.pl)](https://github.com/summanlp/evaluation).

```
from sumeval.metrics.rouge import RougeCalculator


rouge = RougeCalculator(stopwords=True, lang="en")

rouge_1 = rouge.rouge_n(
            summary="I went to the Mars from my living town.",
            references="I went to Mars",
            n=1)

rouge_2 = rouge.rouge_n(
            summary="I went to the Mars from my living town.",
            references=["I went to Mars", "It's my living town"],
            n=2)

rouge_l = rouge.rouge_l(
            summary="I went to the Mars from my living town.",
            references=["I went to Mars", "It's my living town"])

# You need spaCy to calculate ROUGE-BE

rouge_be = rouge.rouge_be(
            summary="I went to the Mars from my living town.",
            references=["I went to Mars", "It's my living town"])

print("ROUGE-1: {}, ROUGE-2: {}, ROUGE-L: {}, ROUGE-BE: {}".format(
    rouge_1, rouge_2, rouge_l, rouge_be
).replace(", ", "\n"))
```

## Install

```
pip install sumeval
```

## Dependencies

* To calculate `ROUGE-BE`, [`spaCy`](https://github.com/explosion/spaCy) is required.
* To use lang `ja`, [`janome`](https://github.com/mocobeta/janome) or [`MeCab`](https://github.com/taku910/mecab) is required.
  * Especially to get score of `ROUGE-BE`, [`CaboCha`](https://github.com/taku910/cabocha) is needed additionally.

## Test

`sumeval` uses two packages to test the score.

* [pythonrouge](https://github.com/tagucci/pythonrouge)
  * It calls original perl script
* [rougescore](https://github.com/bdusell/rougescore)
  * It's simple python implementation for rouge score

## Welcome Contribution :tada:

### Add supported language

The tokenization and dependency parse process for each language is located on `sumeval/metrics/lang`.

You can make language class by inheriting [`BaseLang`](https://github.com/chakki-works/sumeval/blob/master/sumeval/metrics/lang/base_lang.py).
