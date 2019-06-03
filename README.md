<p align="center">
  <img src="https://github.com/chakki-works/sumeval/raw/master/doc/top.png" width="300px">

  <h4 align="center">
    Well tested & Multi-language<br/>
    evaluation framework for Text Summarization.
  </h4>
</p>

[![PyPI version](https://badge.fury.io/py/sumeval.svg)](https://badge.fury.io/py/sumeval)
[![Build Status](https://travis-ci.org/chakki-works/sumeval.svg?branch=master)](https://travis-ci.org/chakki-works/sumeval)
[![codecov](https://codecov.io/gh/chakki-works/sumeval/branch/master/graph/badge.svg)](https://codecov.io/gh/chakki-works/sumeval)


* Well tested
  * The ROUGE-X scores are tested compare with [original Perl script (ROUGE-1.5.5.pl)](https://github.com/summanlp/evaluation).
  * The BLEU score is calculated by [SacréBLEU](https://github.com/awslabs/sockeye/tree/master/contrib/sacrebleu), that produces the same values as official script (`mteval-v13a.pl`) used by WMT.
* Multi-language
  * Not only English, Japanese are also supported. The other language is extensible [easily](https://github.com/chakki-works/sumeval#welcome-contribution-tada).

Of course, implementation is Pure Python!

## How to use

```py
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

```py
from sumeval.metrics.bleu import BLEUCalculator


bleu = BLEUCalculator()
score = bleu.bleu("I am waiting on the beach",
                  "He is walking on the beach")

bleu_ja = BLEUCalculator(lang="ja")
score_ja = bleu_ja.bleu("私はビーチで待ってる", "彼がベンチで待ってる")
```

### From the command line

```
sumeval r-nlb "I'm living New York its my home town so awesome" "My home town is awesome"
```

output.

```
{
  "options": {
    "stopwords": true,
    "stemming": false,
    "word_limit": -1,
    "length_limit": -1,
    "alpha": 0.5,
    "input-summary": "I'm living New York its my home town so awesome",
    "input-references": [
      "My home town is awesome"
    ]
  },
  "averages": {
    "ROUGE-1": 0.7499999999999999,
    "ROUGE-2": 0.6666666666666666,
    "ROUGE-L": 0.7499999999999999,
    "ROUGE-BE": 0
  },
  "scores": [
    {
      "ROUGE-1": 0.7499999999999999,
      "ROUGE-2": 0.6666666666666666,
      "ROUGE-L": 0.7499999999999999,
      "ROUGE-BE": 0
    }
  ]
}
```

Undoubtedly you can use file input. Please see more detail by `sumeval -h`.

## Install

```
pip install sumeval
```

## Dependencies

* BLEU is depends on [SacréBLEU](https://github.com/awslabs/sockeye/tree/master/contrib/sacrebleu)
* To calculate `ROUGE-BE`, [`spaCy`](https://github.com/explosion/spaCy) is required.
* To use lang `ja`, [`janome`](https://github.com/mocobeta/janome) or [`MeCab`](https://github.com/taku910/mecab) is required.
  * Especially to get score of `ROUGE-BE`, [`GiNZA`](https://github.com/megagonlabs/ginza) is needed additionally.
* To use lang `zh`, [`jieba`](https://github.com/fxsjy/jieba) is required.
  * Especially to get score of `ROUGE-BE`, [`pyhanlp`](https://github.com/hankcs/pyhanlp) is needed additionally.

## Test

`sumeval` uses two packages to test the score.

* [pythonrouge](https://github.com/tagucci/pythonrouge)
  * It calls original perl script
  * `pip install git+https://github.com/tagucci/pythonrouge.git`
* [rougescore](https://github.com/bdusell/rougescore)
  * It's simple python implementation for rouge score
  * `pip install git+git://github.com/bdusell/rougescore.git`

## Welcome Contribution :tada:

### Add supported language

The tokenization and dependency parse process for each language is located on `sumeval/metrics/lang`.

You can make language class by inheriting [`BaseLang`](https://github.com/chakki-works/sumeval/blob/master/sumeval/metrics/lang/base_lang.py).
