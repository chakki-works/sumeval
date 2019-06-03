import os
import json
import unittest
from sumeval.metrics.rouge import RougeCalculator


class TestRougeBE(unittest.TestCase):
    DATA_DIR = os.path.join(os.path.dirname(__file__), "data/rouge")

    def load_test_data(self):
        test_file = os.path.join(self.DATA_DIR, "ROUGE-test.json")
        with open(test_file, encoding="utf-8") as f:
            data = json.load(f)
        return data

    def _bes_to_words(self, basic_elements, compare_type):
        words = []
        for be in basic_elements:
            words.append(be.as_key(compare_type))
        return words

    def test_rouge_be(self):
        data = self.load_test_data()
        rouge = RougeCalculator(stopwords=False)
        for eval_id in data:
            summaries = data[eval_id]["summaries"]
            references = data[eval_id]["references"]
            r_bes = [rouge.parse_to_be(r) for r in references]

            for _type in ["H", "HM", "HMR"]:
                print("eval {}: test {} pattern.".format(eval_id, _type))
                _r_bes = [self._bes_to_words(r, _type) for r in r_bes]

                for s in summaries:
                    s_bes = rouge.parse_to_be(s)
                    if len(s_bes) == 0:
                        continue
                    s_bes = self._bes_to_words(s_bes, _type)
                    base = rouge.rouge_n(s_bes, _r_bes, n=1)
                    score = rouge.rouge_be(s, references, _type)
                    self.assertLess(abs(base - score), 1e-5)

    def test_rouge_be_hm(self):
        rouge = RougeCalculator(stopwords=False)
        summaries = [
            "It was beautiful flower, and the other was beautiful flower also."
        ]
        references = [
            "The flower was beautiful.",
            "Two flower were beautiful"
        ]
        r_bes = [rouge.parse_to_be(r) for r in references]

        for _type in ["HM", "HMR"]:
            _r_bes = [self._bes_to_words(r, _type) for r in r_bes]
            for s in summaries:
                s_bes = rouge.parse_to_be(s)
                s_bes = self._bes_to_words(s_bes, _type)
                base = rouge.rouge_n(s_bes, _r_bes, n=1)
                score = rouge.rouge_be(s, references, _type)
                self.assertLess(abs(base - score), 1e-5)


if __name__ == "__main__":
    unittest.main(warnings="ignore")
