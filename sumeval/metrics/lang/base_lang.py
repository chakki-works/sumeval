import os
from pathlib import Path


class BaseLang():
    _PARSER = None

    def __init__(self, lang):
        self.lang = lang
        self._stopwords = []
        self._stemming = {}

    def load_parser(self):
        if self._PARSER is None:
            import spacy
            self._PARSER = spacy.load(self.lang)
        return self._PARSER

    def tokenize(self, text):
        raise Exception("Have to implement tokenize in subclass")

    def parse_to_be(self, text):
        from spacy.symbols import VERB, ADJ
        doc = self.load_parser()(text)
        bes = []
        for chunk in doc.noun_chunks:
            # chunk level dependencies
            if chunk.root.head.pos in [VERB, ADJ]:
                be = BasicElement(chunk.root.text, chunk.root.head.lemma_,
                                  chunk.root.dep_,)
                bes.append(be)

                # in-chunk level dependencies
                for c in chunk.root.children:
                    if c.pos in [VERB, ADJ]:
                        be = BasicElement(chunk.root.text, c.lemma_,
                                          c.dep_)
                        bes.append(be)
        return bes

    def is_stop_word(self, word):
        if len(self._stopwords) == 0:
            self.load_stopwords()
        return word in self._stopwords

    def stemming(self, word, min_length=-1):
        if len(self._stemming) == 0:
            self.load_stemming_dict()

        _word = word
        if min_length > 0 and len(_word) < min_length:
            return _word
        elif _word in self._stemming:
            return self._stemming[_word]
        else:
            return _word
        return _word

    def load_stopwords(self):
        p = Path(os.path.dirname(__file__))
        p = p.joinpath("data", self.lang, "stop_words.txt")
        if p.is_file():
            with p.open(encoding="utf-8") as f:
                lines = f.readlines()
                lines = [ln.strip() for ln in lines]
                lines = [ln for ln in lines if ln]
            self._stopwords = lines

    def load_stemming_dict(self):
        p = Path(os.path.dirname(__file__))
        p = p.joinpath("data", self.lang, "stemming.txt")
        if p.is_file():
            with p.open(encoding="utf-8") as f:
                lines = f.readlines()
                lines = [ln.strip() for ln in lines]
                lines = [ln for ln in lines if ln]
            self._stemming = dict(lines)


class BasicElement():

    def __init__(self, head, modifier, relation):
        self.head = head
        self.modifier = modifier
        self.relation = relation

    def equals(self, other, option="HMR"):
        equal = True
        for c in option:
            c = c.upper()
            if c == "H" and self.head != other.head:
                equal = False
            elif c == "M" and self.modifier != other.modifier:
                equal = False
            elif c == "R" and self.relation != other.relation:
                equal = False
        return equal

    def as_key(self, option="HMR"):
        els = []
        for c in option:
            c = c.upper()
            if c == "H":
                els.append(self.head)
            elif c == "M":
                els.append(self.modifier)
            elif c == "R":
                els.append(self.relation)
        return "|".join(els)

    def __repr__(self):
        return "<BasicElement: {}-[{}]->{}>".format(
                    self.head, self.relation, self.modifier)
