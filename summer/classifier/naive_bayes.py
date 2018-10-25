import pickle
from datetime import datetime

import nltk

from summer.classifier.base import BaseClassifier
from summer.tokenizer import tokenize, F_LOWERCASE


class NaiveBayesClassifier(BaseClassifier):
    def __init__(self, training_data, test_data, *, feature_finder=None):
        self._classifier = None
        self.training_data = training_data
        self.test_data = test_data
        self.feature_finder = feature_finder
        super().__init__()

    def train(self):
        self.logger.debug('Labeling training data...')
        data = get_labeled_review_data(self.training_data, self.feature_finder)
        self.logger.debug('Training classifier...')
        self._classifier = nltk.NaiveBayesClassifier.train(data)

    def classify(self, featureset):
        return self.classifier.classify(featureset=featureset)

    def show_top_features(self, n_features=10):
        self.classifier.show_most_informative_features(n_features)

    @property
    def accuracy(self) -> float:
        data = get_labeled_review_data(self.test_data, self.feature_finder)
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


def get_feature_finder(word_features):
    def find_features(review_words):
        features = {}
        for word in word_features:
            features[word] = word in review_words
        return features

    return find_features


def get_labeled_review_data(reviews, feature_finder):
    return [
        (feature_finder(tokenize(r['text'], clean_filter=F_LOWERCASE)),
         r['sentiment'])
        for r in reviews
    ]
