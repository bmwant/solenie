import nltk

from summer.classifier.base import BaseClassifier


class NaiveBayesClassifier(BaseClassifier):
    def __init__(self, training_data, test_data):
        self.classifier = None
        self.training_data = training_data
        self.test_data = test_data
        super().__init__()

    def train(self):
        self.classifier = nltk.NaiveBayesClassifier.train(self.training_data)

    def predict(self):
        self.classifier.show_most_informative_features(15)

    @property
    def accuracy(self) -> float:
        return nltk.classify.accuracy(self.classifier, self.test_data)
