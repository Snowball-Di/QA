# coding:utf-8
from pyhanlp import HanLP


class Tokens(object):
    """A class to represent a list of tokenized text."""

    def __init__(self, data):
        self.data = data

    def __len__(self):
        """The number of tokens."""
        return len(self.data)

    def words(self, uncased=False):
        """Returns a list of the text of each token"""
        if uncased:
            return [t.lower() for t in self.data]
        else:
            return [t for t in self.data]

    def ngrams(self, n=1, uncased=False, filter_fn=None, as_strings=True):
        """Returns a list of all ngrams from length 1 to n.

        Args:
            n: upper limit of ngram length
            uncased: lower cases text
            filter_fn: user function that takes in an ngram list and returns
              True or False to keep or not keep the ngram
            as_strings: return the ngram as a string vs list
        """
        def _skip(gram):
            if not filter_fn:
                return False
            return filter_fn(gram)

        words = self.words(uncased)
        ngrams = [(s, e + 1)
                  for s in range(len(words))
                  for e in range(s, min(s + n, len(words)))
                  if not _skip(words[s:e + 1])]

        # Concatenate into strings
        if as_strings:
            ngrams = ['{}'.format(' '.join(words[s:e])) for (s, e) in ngrams]

        return ngrams


class Tokenizer:

    def __init__(self):
        HanLP.Config.ShowTermNature = False
        # self.model = HanLP()

    def tokenize(self, text):
        clean_text = text.replace('\n', ' ')
        result = [str(t) for t in HanLP.segment(clean_text)]
        return Tokens(result)


# class Tokenizer:
#
#     def __init__(self, device='cuda:0'):
#         # 默认加载到GPU
#         self.model = LTP(device=device, cache_dir='.model_cache/')
#
#     def tokenize(self, text):
#         clean_text = text.replace('\n', ' ')
#         seg_words, _ = self.model.seg([clean_text])
#         return Tokens(seg_words[0])
#
#     def tokenize_batch(self, text_list):
#         clean_list = [t.replace('\n', ' ') for t in text_list]
#         seg_words_list, _ = self.model.seg(clean_list)
#         return [Tokens(seg_words) for seg_words in seg_words_list]


# 用法
# tok = Tokenizer()
# tokens = tok.tokenize('习近平 '*10)
# print()
# print(tokens.ngrams(n=2))
