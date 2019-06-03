import unittest
from collections import Counter
from sumeval.metrics.lang.lang_en import LangEN


class TestLangEN(unittest.TestCase):

    def test_basic_element(self):
        lang = LangEN()
        text = "The very beautiful toy is bought by Tom."
        bes = lang.parse_to_be(text)
        for i, be in enumerate(bes):
            print(be)
            if i == 0:
                self.assertEqual(be.head, "toy")
                self.assertEqual(be.modifier, "beautiful")
            else:
                self.assertEqual(be.head, "toy")
                self.assertEqual(be.modifier, "buy")

    def test_stemming(self):
        lang = LangEN()
        text = "dippier dippy"
        counts = Counter([lang.stemming(w) for w in lang.tokenize_with_preprocess(text)])
        self.assertEqual(("dippy", 2), counts.most_common()[0])
