import os
import sys
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
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
                self.assertEqual(be.modifier, "buy")
            else:
                self.assertEqual(be.head, "toy")
                self.assertEqual(be.modifier, "beautiful")


if __name__ == "__main__":
    unittest.main(warnings="ignore")
