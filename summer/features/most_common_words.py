import pickle

from nltk.probability import FreqDist

from summer.features.base import BaseFeatureFinder


class MostCommonWordsFinder(BaseFeatureFinder):
    def __init__(self, n_words=None):
        self.n_words = n_words
        self._features = None
        super().__init__()

    def process(self, words):
        fd = FreqDist(words)
        self.logger.debug('Finding features...')
        self._features = [item[0] for item in fd.most_common(self.n_words)]

    def save(self, filename):
        features = self.features
        self.logger.info('Saving %s featureset to %s', self, filename)
        with open(filename, 'wb') as f:
            pickle.dump(features, f)

    @classmethod
    def load(cls, filename):
        with open(filename, 'rb') as f:
            _features = pickle.load(f)
        feature_finder = cls(n_words=len(_features))
        feature_finder._features = _features
        feature_finder.logger.debug(
            'Loaded featureset from file %s.', filename)
        return feature_finder

    def find_features(self, words):
        features = {}
        for word in self.features:
            features[word] = word in words
        return features

    @property
    def features(self):
        if self._features is None:
            raise RuntimeError(
                'Features are unavailable. '
                'Make sure you have called `process`.'
            )
        return self._features

    def __str__(self):
        return f'{self.__class__.__name__}({self.n_words})'
