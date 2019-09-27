import unittest
from sumeval.metrics.lang.base_lang import BaseLang
from sumeval.metrics.rouge import RougeCalculator
from sumeval.metrics.bleu import BLEUCalculator


class TestCustomLang(unittest.TestCase):

    def test_custom_lang(self):

        class Custom(BaseLang):

            def __init__(self):
                super(Custom, self).__init__("cs")
            
            def tokenize(self, text):
                return text.split("/")

        lang = Custom()
        rouge = RougeCalculator(lang=lang)
        rouge_score = rouge.rouge_n(
            summary="I/went/to/the/Mars/from/my/living/town.",
            references="I/went/to/Mars",
            n=1)

        bleu = BLEUCalculator(lang=lang)
        bleu_score = bleu.bleu("I/am/waiting/on/the/beach",
                        "He/is/walking/on/the/beach")

        self.assertGreater(rouge_score, 0)
        self.assertGreater(bleu_score, 0)


if __name__ == "__main__":
    unittest.main()
