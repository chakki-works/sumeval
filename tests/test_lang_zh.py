import unittest
import pytest
from sumeval.metrics.lang.lang_zh import LangZH


class TestLangZH(unittest.TestCase):

    def test_tokenize(self):
        lang = LangZH()
        text = "我发现了一朵非常漂亮的花"
        tokens = lang.tokenize(text)
        self.assertEqual(len(tokens), 8)

    @pytest.mark.skip(reason="Download the parse model is terrible slow.")
    def test_basic_element(self):
        lang = LangZH()
        text = "我发现了一朵非常漂亮的花"
        bes = lang.parse_to_be(text)
        for i, be in enumerate(bes):
            if i == 0:
                self.assertEqual(be.head, "花")
                self.assertEqual(be.modifier, "漂亮")
            else:
                self.assertEqual(be.head, "花")
                self.assertEqual(be.modifier, "发现")
