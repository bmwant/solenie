from abc import ABC, abstractmethod

import numpy as np

import settings
from buttworld.logger import get_logger
from jerry.parser.review import SentimentEnum
from summer.stats import get_text_for_reviews
from summer.tokenizer import _is_sent_terminator
from store import DB, get_reviews_by_sentiment


logger = get_logger(__name__)


class BaseReviewGenerator(ABC):
    @abstractmethod
    def create_good_review(self):
        pass

    @abstractmethod
    def create_bad_review(self):
        pass

    @abstractmethod
    def create_neutral_review(self):
        pass


class SimpleMarkovGenerator(BaseReviewGenerator):
    """
    Based on
    https://towardsdatascience.com/simulating-text-with-markov-chains-in-python-1a27e6d13fc6
    """
    def __init__(self, text):
        self._text_good = text.split()
        self.word_dict_good = {}
        self.word_dict_neutral = {}
        self.word_dict_bad = {}

    def initialize(self):
        logger.info('Initializing words dictionaries...')
        pairs = self.make_pairs(self._text_good)
        # todo (misha): defaultdict
        for first, second in pairs:
            if first in self.word_dict_good:
                self.word_dict_good[first].append(second)
            else:
                self.word_dict_good[first] = [second]

    def make_pairs(self, text):
        for i in range(len(text)-1):
            yield (text[i], text[i+1])

    def get_first_word(self):
        while True:
            first_word = np.random.choice(self._text_good)
            char = first_word[0]
            if char.isalnum() and char.isupper():
                return first_word

    def create_good_review(self):
        min_length = 40
        first_word = self.get_first_word()
        chain = [first_word]
        while True:
            next_word = np.random.choice(self.word_dict_good[chain[-1]])
            chain.append(next_word)
            char = next_word[-1]
            if len(chain) > min_length and _is_sent_terminator(char):
                break
        return ' '.join(chain)

    def create_neutral_review(self):
        return ''

    def create_bad_review(self):
        return ''


if __name__ == '__main__':
    db = DB(settings.TOP_500_MOVIE_REVIEWS)
    reviews = get_reviews_by_sentiment(SentimentEnum.GOOD, db=db)
    text = get_text_for_reviews(reviews)
    gen = SimpleMarkovGenerator(text)
    gen.initialize()
    print(gen.create_good_review())
