import unittest
from sumeval.metrics.bleu import BLEUCalculator


class TestBLEU(unittest.TestCase):

    def test_bleu(self):
        bleu = BLEUCalculator()
        score = bleu.bleu("I am waiting on the beach",
                          "He is walking on the beach",)
        score_from_list = bleu.bleu("I am waiting on the beach".split(),
                                    ["He is walking on the beach".split()])
        self.assertLess(abs(score - score_from_list), 1e-8)

        bleu = BLEUCalculator(lang="ja")
        score_ja = bleu.bleu("私はビーチで待ってる", "彼がベンチで待ってる")

        self.assertLess(abs(score - score_ja), 1e-8)


if __name__ == "__main__":
    unittest.main(warnings="ignore")
