from string import punctuation
from itertools import filterfalse

from nltk.tokenize import sent_tokenize, word_tokenize


EXTRA_PUNCTUATION = '«»—…'


def _is_punctuation(token):
    _punctuation = {*punctuation, *EXTRA_PUNCTUATION}
    return token in _punctuation


def clean_tokens(tokens):
    lowercase = map(str.lower, tokens)
    return filterfalse(_is_punctuation, lowercase)


def tokenize(text, clean=True):
    words = []
    for sentence in sent_tokenize(text):
        for word in word_tokenize(sentence):
            words.append(word)

    if clean:
        return list(clean_tokens(words))
    return words
