from string import punctuation
from itertools import filterfalse

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords


EXTRA_PUNCTUATION = '«»—…'
TERMINATION_CHARS = '.»…!?)"\''


def _is_sent_terminator(token):
    return token in TERMINATION_CHARS


def _is_punctuation(token):
    _punctuation = {*punctuation, *EXTRA_PUNCTUATION}
    return token in _punctuation


def _is_stopword(token, language='russian'):
    return token in stopwords.words(language)


def clean_tokens(tokens):
    lowercase = map(str.lower, tokens)
    punct_removed = filterfalse(_is_punctuation, lowercase)
    return filterfalse(_is_stopword, punct_removed)


def tokenize(text, clean=True):
    words = []
    for sentence in sent_tokenize(text):
        for word in word_tokenize(sentence):
            words.append(word)

    if clean:
        return list(clean_tokens(words))
    return words
