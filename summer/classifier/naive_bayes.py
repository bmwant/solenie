import pickle
from datetime import datetime

import nltk

from summer.classifier.base import BaseClassifier
from summer.tokenizer import tokenize, F_LOWERCASE


class NaiveBayesClassifier(BaseClassifier):
    def __init__(self):
        self._classifier = None
        super().__init__()

    def train(self, data):
        self.logger.debug('Training classifier...')
        self._classifier = nltk.NaiveBayesClassifier.train(data)

    def classify(self, featureset):
        return self.classifier.classify(featureset=featureset)

    def show_top_features(self, n_features=10):
        self.classifier.show_most_informative_features(n_features)

    def accuracy(self, data) -> float:
        return nltk.classify.accuracy(self.classifier, data)

    @property
    def classifier(self):
        if self._classifier is None:
            raise RuntimeError('Classifier has not been trained yet')
        return self._classifier

    def save(self):
        now = datetime.now()
        name = self.__class__.__name__.lower()
        day = now.strftime('%Y%m%d')
        model_filename = '{}_{}.classifier'.format(name, day)
        classifier = self.classifier
        self.logger.info('Saving trained classifier to %s', model_filename)
        with open(model_filename, 'wb') as f:
            pickle.dump(classifier, f)

    @classmethod
    def load(cls, filename):
        with open(filename, 'rb') as f:
            _classifier = pickle.load(f)
        classifier = cls()
        classifier.logger.debug('Loaded classifier from file %s.', filename)
        classifier._classifier = _classifier
        return classifier


def get_labeled_review_data(reviews, feature_finder):
    return [
        (feature_finder(tokenize(r['text'], clean_filter=F_LOWERCASE)),
         r['sentiment'])
        for r in reviews
    ]
