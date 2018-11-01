import pickle
from datetime import datetime

import settings
from summer.classifier.base import BaseClassifier

from nltk.classify.scikitlearn import SklearnClassifier



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
        name = self.name.lower()
        model_filename = '{}_{}.classifier'.format(name, day)
        self.logger.info('Saving trained classifier to %s', model_filename)
        path = settings.TRAINED_CLASSIFIERS_DIR / model_filename
        with open(path, 'wb') as f:
            pickle.dump(data, f)

    @classmethod
    def load(cls, filename):
        path = settings.TRAINED_CLASSIFIERS_DIR / filename
        with open(path, 'rb') as f:
            data = pickle.load(f)
        classifier = cls(data['clf'])
        classifier._vectorizer = data['vectorizer']
        classifier._encoder = data['encoder']
        classifier.logger.debug('Loaded classifier from file %s', filename)
        return classifier

    @property
    def name(self):
        return self._clf.__class__.__name__


def main():



    # 0.8461
    # LinearSVC_classifier = SklearnClassifier(LinearSVC())
    # LinearSVC_classifier.train(train_data)
    # print("LinearSVC_classifier accuracy percent:",
    #       nltk.classify.accuracy(LinearSVC_classifier, test_data))
    pass


if __name__ == '__main__':
    main()
