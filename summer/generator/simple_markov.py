from collections import defaultdict

import numpy as np

from jerry.parser.review import SentimentEnum
from summer.tokenizer import _is_sent_terminator
from summer.generator.base import BaseReviewGenerator


DEFAULT_MIN_REVIEW_LENGTH = 40


class SimpleMarkovGenerator(BaseReviewGenerator):
    """
    Based on
    https://towardsdatascience.com/simulating-text-with-markov-chains-in-python-1a27e6d13fc6
    """
    def __init__(self, min_length=DEFAULT_MIN_REVIEW_LENGTH):
        self.min_length = min_length
        self._text_good = []
        self._text_neutral = []
        self._text_bad = []
        self.word_dict_good = defaultdict(list)
        self.word_dict_neutral = defaultdict(list)
        self.word_dict_bad = defaultdict(list)
        super().__init__()

    def initialize_model(self, sentiment: SentimentEnum, text: str):
        self.logger.info('Initializing model for %s...', sentiment)
        text_chunks = text.split()
        suffix = sentiment.name.lower()
        setattr(self, f'_text_{suffix}', text_chunks)
        pairs = self.make_pairs(getattr(self, f'_text_{suffix}'))
        word_dict = getattr(self, f'word_dict_{suffix}')
        for first, second in pairs:
            word_dict[first].append(second)

    def make_pairs(self, text):
        for i in range(len(text)-1):
            yield (text[i], text[i+1])

    def get_first_word(self, text_chunks):
        while True:
            first_word = np.random.choice(text_chunks)
            char = first_word[0]
            if char.isalnum() and char.isupper():
                return first_word

    def _create_review(self, sentiment: SentimentEnum, min_length: int):
        suffix = sentiment.name.lower()
        word_dict = getattr(self, f'word_dict_{suffix}')
        text_chunks = getattr(self, f'_text_{suffix}')
        first_word = self.get_first_word(text_chunks)

        chain = [first_word]
        while True:
            next_word = np.random.choice(word_dict[chain[-1]])
            chain.append(next_word)
            char = next_word[-1]
            if len(chain) > min_length and _is_sent_terminator(char):
                break
        return ' '.join(chain)

    def create_good_review(self, length=None):
        min_length = length or self.min_length
        if not self.word_dict_good:
            raise RuntimeError(
                'Generator is not initialized with good reviews data')
        return self._create_review(SentimentEnum.GOOD, min_length)

    def create_neutral_review(self, length=None):
        min_length = length or self.min_length
        if not self.word_dict_neutral:
            raise RuntimeError(
                'Generator is not initialized with neutral reviews data')
        return self._create_review(SentimentEnum.NEUTRAL, min_length)

    def create_bad_review(self, length=None):
        min_length = length or self.min_length
        if not self.word_dict_bad:
            raise RuntimeError(
                'Generator is not initialized with bad reviews data')
        return self._create_review(SentimentEnum.BAD, min_length)
