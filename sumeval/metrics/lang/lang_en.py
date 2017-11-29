import re
from sumeval.metrics.lang.base_lang import BaseLang


class LangEN(BaseLang):

    def __init__(self):
        super().__init__("en")
        self._symbol_replace = re.compile(r"[^A-Za-z0-9-]")
        self._valid_word = re.compile(r"^[A-Za-z0-9$]")

    def tokenize(self, text):
        _txt = self._format_text(text)
        words = _txt.split(" ")
        words = [w.strip() for w in words if w.strip()]
        words = [w for w in words if self._valid_word.match(w)]
        return words

    def _format_text(self, text):
        _txt = text.replace("-", " - ")
        _txt = self._symbol_replace.sub(" ", _txt)
        _txt = _txt.strip()
        return _txt

    def parse_to_be(self, text):
        _txt = self._format_text(text)
        bes = super().parse_to_be(_txt)

        def is_valid(be):
            if self._valid_word.match(be.head) and\
               self._valid_word.match(be.modifier):
                return True
            else:
                return False

        bes = [be for be in bes if is_valid(be)]
        return bes
