from collections import Counter
from sumeval.metrics.lang.base_lang import BaseLang
from sumeval.metrics.lang import get_lang


class RougeCalculator():

    def __init__(self,
                 stopwords=True, stemming=False,
                 word_limit=-1, length_limit=-1,
                 measure='f1', lang="en"):
        self.stemming = stemming
        self.stopwords = stopwords
        self.word_limit = word_limit
        self.length_limit = length_limit
        self.measure = measure.lower()
        if isinstance(lang, str):
            self.lang = lang
            self._lang = get_lang(lang)
        elif isinstance(lang, BaseLang):
            self.lang = lang.lang
            self._lang = lang

    def tokenize(self, text_or_words, is_reference=False):
        """
        Tokenize a text under original Perl script manner.

        Parameters
        ----------
        text_or_words: str or str[]
            target text or tokenized words.
            If you use tokenized words, preprocessing is not applied.
            It allows you to calculate ROUGE under your customized tokens,
            but you have to pay attention to preprocessing.
        is_reference: bool
            for reference process or not

        See Also
        --------
        https://github.com/andersjo/pyrouge/blob/master/tools/ROUGE-1.5.5/ROUGE-1.5.5.pl#L1820
        """
        words = text_or_words

        def split(text):
            _words = self._lang.tokenize(text)
            return _words

        if self.word_limit > 0:
            if isinstance(words, str):
                words = split(words)
            words = words[:self.word_limit]
            words = self._lang.join(words)
        elif self.length_limit > 0:
            text = words
            if isinstance(text, (list, tuple)):
                text = self._lang.join(words)
            words = text[:self.length_limit]

        if isinstance(words, str):
            words = self._lang.tokenize_with_preprocess(words)

        words = [w.lower().strip() for w in words if w.strip()]

        if self.stopwords:
            words = [w for w in words if not self._lang.is_stop_word(w)]

        if self.stemming and is_reference:
            # stemming is only adopted to reference
            # https://github.com/andersjo/pyrouge/blob/master/tools/ROUGE-1.5.5/ROUGE-1.5.5.pl#L1416

            # min_length ref
            # https://github.com/andersjo/pyrouge/blob/master/tools/ROUGE-1.5.5/ROUGE-1.5.5.pl#L2629
            words = [self._lang.stemming(w, min_length=3) for w in words]
        return words

    def parse_to_be(self, text, is_reference=False):
        bes = self._lang.parse_to_be(text)

        def preprocess(be):
            be.head = be.head.lower().strip()
            be.modifier = be.modifier.lower().strip()
            if self.stemming and is_reference:
                be.head = self._lang.stemming(be.head, min_length=3)
                be.modifier = self._lang.stemming(be.modifier, min_length=3)

            return be

        bes = [preprocess(be) for be in bes]
        return bes

    def len_ngram(self, words, n):
        return max(len(words) - n + 1, 0)

    def ngram_iter(self, words, n):
        for i in range(self.len_ngram(words, n)):
            n_gram = words[i:i+n]
            yield tuple(n_gram)

    def count_ngrams(self, words, n):
        c = Counter(self.ngram_iter(words, n))
        return c

    def count_overlap(self, summary_ngrams, reference_ngrams):
        result = 0
        for k, v in summary_ngrams.items():
            result += min(v, reference_ngrams[k])
        return result

    def rouge_1(self, summary, references, alpha=0.5):
        return self.rouge_n(summary, references, 1, alpha)

    def rouge_2(self, summary, references, alpha=0.5):
        return self.rouge_n(summary, references, 2, alpha)

    def rouge_n(self, summary, references, n, alpha=0.5):
        """
        Calculate ROUGE-N score.

        Parameters
        ----------
        summary: str
            summary text
        references: str or str[]
            reference or references to evaluate summary
        n: int
            ROUGE kind. n=1, calculate when ROUGE-1
        alpha: float (0~1)
            alpha -> 0: recall is more important
            alpha -> 1: precision is more important
            F = 1/(alpha * (1/P) + (1 - alpha) * (1/R))

        Returns
        -------
        score: float
            measured score
        """
        _summary = self.tokenize(summary)
        summary_ngrams = self.count_ngrams(_summary, n)
        _refs = [references] if isinstance(references, str) else references
        matches = 0
        count_for_recall = 0
        for r in _refs:
            _r = self.tokenize(r, True)
            r_ngrams = self.count_ngrams(_r, n)
            matches += self.count_overlap(summary_ngrams, r_ngrams)
            count_for_recall += self.len_ngram(_r, n)
        count_for_prec = len(_refs) * self.len_ngram(_summary, n)
        score = self._calc_score(matches, count_for_recall, count_for_prec, alpha)
        return score

    def _calc_score(self, matches, count_for_recall, count_for_precision, alpha):
        def safe_div(x1, x2):
            return 0 if x2 == 0 else x1 / x2
        if self.measure == 'recall':
            recall = safe_div(matches, count_for_recall)
            return recall
        if self.measure == "precision":
            precision = safe_div(matches, count_for_precision)
            return precision
        if self.measure == "f1":
            precision = safe_div(matches, count_for_precision)
            recall = safe_div(matches, count_for_recall)
            denom = (1.0 - alpha) * precision + alpha * recall
            return safe_div(precision * recall, denom)
        raise ValueError(f"measure option should be recall, precision, or f1 but got {self.measure}")

    def lcs(self, a, b):
        longer = a
        base = b
        if len(longer) < len(base):
            longer, base = base, longer

        if len(base) == 0:
            return 0

        row = [0] * len(base)
        for c_a in longer:
            left = 0
            upper_left = 0
            for i, c_b in enumerate(base):
                up = row[i]
                if c_a == c_b:
                    value = upper_left + 1
                else:
                    value = max(left, up)
                row[i] = value
                left = value
                upper_left = up

        return left

    def rouge_l(self, summary, references, alpha=0.5):
        """
        Calculate ROUGE-L score.

        Parameters
        ----------
        summary: str
            summary text
        references: str or str[]
            reference or references to evaluate summary
        alpha: float (0~1)
            alpha -> 0: recall is more important
            alpha -> 1: precision is more important
            F = 1/(alpha * (1/P) + (1 - alpha) * (1/R))
        
        Returns
        -------
        f1: float
            f1 score
        """
        matches = 0
        count_for_recall = 0
        _summary = self.tokenize(summary)
        _refs = [references] if isinstance(references, str) else references
        for r in _refs:
            _r = self.tokenize(r, True)
            matches += self.lcs(_r, _summary)
            count_for_recall += len(_r)
        count_for_prec = len(_refs) * len(_summary)
        score = self._calc_score(matches, count_for_recall, count_for_prec, alpha)
        return score

    def count_be(self, text, compare_type, is_reference=False):
        bes = self.parse_to_be(text, is_reference)
        be_keys = [be.as_key(compare_type) for be in bes]
        c = Counter(be_keys)
        return c

    def rouge_be(self, summary, references, compare_type="HMR", alpha=0.5):
        """
        Calculate ROUGE-BE score.

        Parameters
        ----------
        summary: str
            summary text
        references: str or str[]
            reference or references to evaluate summary
        compare_type: str
            "H", "M", "R" or these combination.
            Each character means basic element component.
            H: head, M: modifier, R: relation.
            The image of these relation is following.
            {head word}-{relation}->{modifier word}
            When "HMR", use head-relation-modifier triple as basic element.
        alpha: float (0~1)
            alpha -> 0: recall is more important
            alpha -> 1: precision is more important
            F = 1/(alpha * (1/P) + (1 - alpha) * (1/R))
        
        Returns
        -------
        f1: float
            f1 score
        """
        matches = 0
        count_for_recall = 0
        s_bes = self.count_be(summary, compare_type)
        _refs = [references] if isinstance(references, str) else references
        for r in _refs:
            r_bes = self.count_be(r, compare_type, True)
            matches += self.count_overlap(s_bes, r_bes)
            count_for_recall += sum(r_bes.values())
        count_for_prec = len(_refs) * sum(s_bes.values())
        score = self._calc_score(matches, count_for_recall, count_for_prec, alpha)
        return score
