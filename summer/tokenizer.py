from string import punctuation
from itertools import filterfalse
from functools import partial

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

from buttworld.logger import get_logger


logger = get_logger(__name__)

EXTRA_PUNCTUATION = '«»—…'
TERMINATION_CHARS = '.»…!?)"\''


F_LOWERCASE     = 0b00001
F_PUNCTUATION   = 0b00010
F_STOPWORD      = 0b00100
F_NUMBER        = 0b01000

FILTER_NONE     = 0b00000
FILTER_ALL      = F_LOWERCASE | F_PUNCTUATION | F_STOPWORD | F_NUMBER


def _is_sent_terminator(token):
    return token in TERMINATION_CHARS


def _is_number(token):
    try:
        float(token.replace(',', '.'))
    except ValueError:
        return False
    return True


def _is_punctuation(token):
    _punctuation = {*punctuation, *EXTRA_PUNCTUATION}
    return token in _punctuation


def _is_stopword(token, language='russian'):
    return token in stopwords.words(language)


def clean_tokens(tokens, clean_filter, language='english'):
    if F_LOWERCASE & clean_filter:
        tokens = map(str.lower, tokens)
    if F_PUNCTUATION & clean_filter:
        tokens = filterfalse(_is_punctuation, tokens)
    if F_NUMBER & clean_filter:
        tokens = filterfalse(_is_number, tokens)
    if F_STOPWORD & clean_filter:
        stopwords_filter = partial(_is_stopword, language=language)
        tokens = filterfalse(stopwords_filter, tokens)
    return tokens


def tokenize(text, clean_filter=FILTER_ALL, language='english'):
    words = []
    for sentence in sent_tokenize(text):
        for word in word_tokenize(sentence):
            words.append(word)

    if clean_filter:
        return list(clean_tokens(words, clean_filter, language=language))
    return words
