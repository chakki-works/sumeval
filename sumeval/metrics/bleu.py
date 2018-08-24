from sacrebleu import corpus_bleu, TOKENIZERS, DEFAULT_TOKENIZER
from sumeval.metrics.lang import get_lang


class BLEUCalculator():

    def __init__(self,
                 smooth="floor", smooth_floor=0.01,
                 lowercase=False, use_effective_order=True,
                 lang="en", tokenizer=DEFAULT_TOKENIZER):
        self.smooth = smooth
        self.smooth_floor = smooth_floor
        self.lowercase = lowercase
        self.use_effective_order = use_effective_order
        self.lang = get_lang(lang)
        self.tokenizer = tokenizer
        if lang == "ja":
            def tokenizer_ja(text):
                words = self.lang.tokenize_with_preprocess(text)
                return " ".join(words)

            TOKENIZERS["ja"] = tokenizer_ja
            self.tokenizer = "ja"

    def bleu(self, summary, references, score_only=True):
        """
        Calculate BLEU score by sacrebleu.

        Parameters
        ----------
        summary: str
            summary text
        references: str or str[]
            reference or references to evaluate summary
        score_only: bool
            when True, return only score

        See Also
        --------
        https://github.com/mjpost/sacreBLEU
        """
        if isinstance(summary, str):
            _s = summary
            _refs = references
            if isinstance(references, list):
                _s = [_s]
                _refs = [references]
            bleu = corpus_bleu(
                    _s, _refs,
                    smooth=self.smooth, smooth_floor=self.smooth_floor,
                    force=False, lowercase=self.lowercase,
                    tokenize=self.tokenizer,
                    use_effective_order=self.use_effective_order)
        else:
            _s = " ".join(summary)
            _refs = [[" ".join(r) for r in references]]
            # already tokenized summary and references
            bleu = corpus_bleu(
                    _s, _refs,
                    smooth=self.smooth, smooth_floor=self.smooth_floor,
                    force=True, lowercase=self.lowercase,
                    tokenize="none",
                    use_effective_order=self.use_effective_order)

        if score_only:
            return bleu.score
        else:
            return bleu
