import re
from sumeval.metrics.lang.base_lang import BaseLang, BasicElement


class LangJA(BaseLang):

    def __init__(self):
        super().__init__("ja")
        self._set_tokenizer()
        self._symbol_replace = re.compile(r"[^ぁ-んァ-ン一-龥ーa-zA-Zａ-ｚＡ-Ｚ0-9０-９]")

    def load_parser(self):
        if self._PARSER is None:
            import CaboCha
            self._PARSER = CaboCha.Parser("-f1")
        return self._PARSER

    def _set_tokenizer(self):
        try:
            import MeCab

            class Tokenizer():

                def __init__(self):
                    self.tagger = MeCab.Tagger("-Ochasen")

                def tokenize(self, text):
                    self.tagger.parse("")
                    node = self.tagger.parseToNode(text)
                    tokens = []
                    while node:
                        if node.surface:
                            tokens.append(node)
                        node = node.next
                    return tokens

            self.tokenizer = Tokenizer()

        except Exception as ex:
            from janome.tokenizer import Tokenizer
            self.tokenizer = Tokenizer()

    def tokenize(self, text):
        _txt = self._symbol_replace.sub(" ", text)
        words = [t.surface for t in self.tokenizer.tokenize(_txt)]
        words = [w.strip() for w in words if w.strip()]
        return words

    def parse_dependency_tree(self, text):
        _txt = self._symbol_replace.sub(" ", text)
        tree = self.load_parser().parse(_txt)

        # get chunks
        chunks = []
        _chunk = []
        for i in range(tree.size()):
            t = tree.token(i)
            m = Morph.create(t)
            if t.chunk:
                if t.chunk.link > -1:
                    m.relation = t.chunk.link
                else:
                    m.is_root = True
                if len(_chunk) > 0:
                    c = Chunk(_chunk)
                    chunks.append(c)
                    _chunk = []
            _chunk.append(m)
        else:
            if len(_chunk) > 0:
                c = Chunk(_chunk)
                chunks.append(c)

        for c in chunks:
            if c.root.has_relation:
                root_head = chunks[c.root.relation].root
                c.root.head = root_head

        return chunks

    def parse_to_be(self, text):
        chunks = self.parse_dependency_tree(text)
        bes = []
        for c in chunks:
            if c.root.head is not None:
                if c.root.head.semantic_pos == "動詞":
                    be = BasicElement(
                        c.root_text,
                        c.root.head.lemma,
                        ""
                    )  # cabocha does not have relation text
                    bes.append(be)
                elif c.root.semantic_pos in ["形容詞", "形容動詞"]:
                    be = BasicElement(
                        c.root.head.lemma,
                        c.root_text,
                        ""
                    )  # cabocha does not have relation text
                    bes.append(be)

        return bes


class Morph():

    def __init__(self, surface, lemma, pos, pos1,
                 relation=-1, head=None, is_root=False):
        self.surface = surface
        self.lemma = lemma
        self.pos = pos
        self.pos1 = pos1
        self.relation = relation
        self.head = head
        self.is_root = is_root

    @property
    def has_relation(self):
        return self.relation > -1

    @property
    def semantic_pos(self):
        if self.pos == "名詞" and self.pos1 in ["形容動詞語幹", "ナイ形容詞語幹"]:
            return "形容動詞"
        else:
            return self.pos

    def __str__(self):
        s = "{}/{}:{},{}".format(
            self.surface, self.lemma, self.pos, self.pos1)
        return s

    def __repr__(self):
        return "<Morph: {}:{}>".format(
                    self.surface, self.pos)

    @classmethod
    def create(cls, token):
        surface = token.surface
        features = token.feature.split(",")
        lemma = features[6]
        pos = features[0]
        pos1 = features[1]
        return Morph(surface, lemma, pos, pos1)


class Chunk():

    def __init__(self, morphs):
        self.morphs = morphs

    @property
    def text(self):
        texts = "".join([m.surface for m in self.morphs])
        return texts

    @property
    def root(self):
        return self.morphs[0]

    @property
    def root_text(self):
        root = self.morphs[0]
        if root.pos == "名詞":
            root_range = 1
            for i in range(len(self.morphs) - 1):
                m = self.morphs[i + 1]
                m_prev = self.morphs[i]
                if m.pos1 in ["固有名詞", "数"] and m.pos1 == m_prev.pos1:
                    root_range += 1
                elif m.pos1 == "接尾":
                    root_range += 1
                    break
                elif m.pos1 == "サ変接続" or m_prev == "サ変接続":
                    root_range += 1
                else:
                    break
            root_text = "".join([m.surface for m in self.morphs[:root_range]])
            return root_text

        else:
            return root.surface

    def __str__(self):
        return self.text

    def __repr__(self):
        s = str(self)
        return "<Chunk: {}>".format(s)
