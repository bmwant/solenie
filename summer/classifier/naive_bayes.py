import nltk

from summer.classifier.base import BaseClassifier
from summer.stats import get_text_for_reviews, get_most_common_words
from summer.tokenizer import tokenize, F_LOWERCASE


class NaiveBayesClassifier(BaseClassifier):
    def __init__(self, training_data, test_data):
        self.classifier = None
        self.training_data = training_data
        self.test_data = test_data
        super().__init__()

    def train(self):
        self.logger.debug('Labeling training data...')
        data = get_labeled_review_data(self.training_data)
        self.logger.debug('Training classifier...')
        self.classifier = nltk.NaiveBayesClassifier.train(data)

    def classify(self, featureset):
        return self.classifier.classify(featureset=featureset)

    def show_top_features(self, n_features=10):
        self.classifier.show_most_informative_features(n_features)

    @property
    def accuracy(self) -> float:
        data = get_labeled_review_data(self.test_data)
        return nltk.classify.accuracy(self.classifier, data)


def get_features(word_features):
    def find_features(review_words):
        features = {}
        for word in word_features:
            features[word] = word in review_words
        return features

    return find_features


def get_labeled_review_data(reviews):
    text = get_text_for_reviews(reviews)
    word_features = get_most_common_words(text, n_words=30)
    find_features = get_features(word_features)
    return [
        (find_features(tokenize(r['text'], clean_filter=F_LOWERCASE)),
         r['sentiment'])
        for r in reviews
    ]

