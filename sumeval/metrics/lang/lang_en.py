import re
from sumeval.metrics.lang.base_lang import BaseLang


class LangEN(BaseLang):

    def __init__(self):
        super(LangEN, self).__init__("en")
        self._symbol_replace = re.compile(r"[^A-Za-z0-9-]")
        self._valid_word = re.compile(r"^[A-Za-z0-9$]")
        self.space_length = 1

    def tokenize(self, text):
        return text.split(" ")

    def tokenize_with_preprocess(self, text):
        _text = self._preprocess(text)
        words = self.tokenize(_text)
        words = [w.strip() for w in words if w.strip()]
        words = [w for w in words if self._valid_word.match(w)]
        return words

    def _preprocess(self, text):
        _text = text.replace("-", " - ")
        _text = self._symbol_replace.sub(" ", _text)
        _text = _text.strip()
        return _text

    def parse_to_be(self, text):
        _text = self._preprocess(text)
        bes = super().parse_to_be(_text)

        def is_valid(be):
            if self._valid_word.match(be.head) and\
               self._valid_word.match(be.modifier):
                return True
            else:
                return False

        bes = [be for be in bes if is_valid(be)]
        return bes
