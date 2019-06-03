import os
import re
from sumeval.metrics.lang.base_lang import BaseLang, BasicElement


class LangZH(BaseLang):

    def __init__(self):
        super(LangZH, self).__init__("zh")
        self._symbol_replace = re.compile(r"[\.\!/_,$%\^\*\(\)\+\“\’\—\!。：？、，：:~@#￥&（）【】「」《》·]")
        import jieba
        self.tokenizer = jieba

    def load_parser(self):
        if self._PARSER is None:
            from pyhanlp import HanLP
            self._PARSER = HanLP.parseDependency
        return self._PARSER

    def tokenize(self, text):
        _text = self._preprocess(text)
        words = [t for t in self.tokenizer.cut(_text, cut_all=False)]
        return words

    def _preprocess(self, text):
        return self._symbol_replace.sub(" ", text)

    def parse_to_be(self, text):
        _text = self._preprocess(text)
        parsed = self.load_parser()(_text)
        bes = []
        for token in parsed.iterator():
            # print(f"{token.NAME}=({token.DEPREL})>{token.HEAD.LEMMA}")
            if token.POSTAG == "n" and token.HEAD.POSTAG in ["v", "a"]:
                be = BasicElement(token.NAME, token.HEAD.LEMMA,
                                  token.DEPREL)
                bes.append(be)
            elif token.POSTAG in ["v", "a"] and token.HEAD.POSTAG == "n":
                be = BasicElement(token.HEAD.NAME, token.LEMMA,
                                  token.DEPREL)
                bes.append(be)

        return bes
