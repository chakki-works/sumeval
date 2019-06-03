import unittest
from sumeval.metrics.lang.lang_ja import LangJA


class TestLangJA(unittest.TestCase):

    def test_basic_element(self):
        lang = LangJA()
        text = "とても綺麗な花を見つけた"
        bes = lang.parse_to_be(text)
        for i, be in enumerate(bes):
            print(be)
            if i == 0:
                self.assertEqual(be.head, "花")
                self.assertEqual(be.modifier, "奇麗")
            else:
                self.assertEqual(be.head, "花")
                self.assertEqual(be.modifier, "見付ける")


if __name__ == "__main__":
    unittest.main()
