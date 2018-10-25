import markovify

from froppyland.enums import SentimentEnum
from summer.generator.base import BaseReviewGenerator


DEFAULT_MAX_SENTENCE_LENGTH = 80
DEFAULT_SENTENCES_IN_REVIEW = 5


class MarkovifyReviewGenerator(BaseReviewGenerator):
    def __init__(self):
        self._model_good = None
        self._model_neutral = None
        self._model_bad = None
        self.sentence_length = DEFAULT_MAX_SENTENCE_LENGTH
        self.sentence_count = DEFAULT_SENTENCES_IN_REVIEW
        super().__init__()

    def initialize_model(self, sentiment: SentimentEnum, text: str):
        suffix = sentiment.name.lower()
        self.logger.info('Initializing model for %s...', sentiment)
        model = markovify.Text(text)
        setattr(self, f'_model_{suffix}', model)

    def _create_review(self, sentiment: SentimentEnum, length=None):
        suffix = sentiment.name.lower()
        model = getattr(self, f'_model_{suffix}')
        if model is None:
            raise RuntimeError(f'{sentiment} model has not been initialized')
        length = length or self.sentence_length
        return ' '.join([
            model.make_short_sentence(max_chars=length)
            for _ in range(self.sentence_count)
        ])

    def create_good_review(self, length=None):
        return self._create_review(SentimentEnum.GOOD, length=length)

    def create_neutral_review(self, length=None):
        return self._create_review(SentimentEnum.NEUTRAL, length=length)

    def create_bad_review(self, length=None):
        return self._create_review(SentimentEnum.BAD, length=length)
