import pickle
from datetime import datetime

from summer.classifier.base import BaseClassifier

from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC


class ScikitClassifierWrapper(SklearnClassifier, BaseClassifier):
    def __init__(self, *args, **kwargs):
        SklearnClassifier.__init__(self, *args, **kwargs)
        BaseClassifier.__init__(self)

    def save(self):
        now = datetime.now()
        # todo (misha): I guess dumping self will be sufficient
        data = {
            'clf': self._clf,
            'vectorizer': self._vectorizer,
            'encoder': self._encoder,
        }
        day = now.strftime('%Y%m%d')
        name = self._clf.__class__.__name__.lower()
        model_filename = '{}_{}.classifier'.format(name, day)
        self.logger.info('Saving trained classifier to %s', model_filename)
        with open(model_filename, 'wb') as f:
            pickle.dump(data, f)

    @classmethod
    def load(cls, filename):
        with open(filename, 'rb') as f:
            data = pickle.load(f)
        classifier = cls(data['clf'])
        classifier._vectorizer = data['vectorizer']
        classifier._encoder = data['encoder']
        classifier.logger.debug('Loaded classifier from file %s', filename)
        return classifier


def main():

    # BNB_classifier.train(train_data)
    # print("BernoulliNB accuracy percent:",
    #       nltk.classify.accuracy(BNB_classifier, test_data))

    # Looks good
    # Fix warnings
    # LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
    # LogisticRegression_classifier.train(train_data)
    # print("LogisticRegression_classifier accuracy percent:",
    #       nltk.classify.accuracy(LogisticRegression_classifier, test_data))

    # 0.8547
    # SGDClassifier_classifier = SklearnClassifier(SGDClassifier())
    # SGDClassifier_classifier.train(train_data)
    # print("SGDClassifier_classifier accuracy percent:",
    #       nltk.classify.accuracy(SGDClassifier_classifier, test_data))


    # 0.9188!!
    # Fix warnings
    # SVC_classifier = SklearnClassifier(SVC())
    # SVC_classifier.train(train_data)
    # print("SVC_classifier accuracy percent:",
    #       nltk.classify.accuracy(SVC_classifier, test_data))

    # 0.8461
    # LinearSVC_classifier = SklearnClassifier(LinearSVC())
    # LinearSVC_classifier.train(train_data)
    # print("LinearSVC_classifier accuracy percent:",
    #       nltk.classify.accuracy(LinearSVC_classifier, test_data))
    pass


if __name__ == '__main__':
    main()
