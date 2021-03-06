from typing import Iterable

import nltk
from terminaltables.other_tables import SingleTable

import settings
from store import DB, get_reviews
from buttworld.logger import get_logger
from froppyland.enums import SentimentEnum
from summer.features import MostCommonWordsFinder
from summer.partitioner import DistributionPartitioner
from summer.classifier.naive_bayes import get_labeled_review_data


class ClassifierComparator(object):
    def __init__(self, classifiers: Iterable):
        self.train_data = None
        self.test_data = None
        self.classifiers = classifiers
        self.logger = get_logger(self.__class__.__name__.lower())

    def train_classifiers(self, save_trained=True):
        for classifier in self.classifiers:
            self.logger.info('Training classifier %s', classifier)
            try:
                classifier.train(self.train_data)
            except Exception as e:
                print(classifier.name, 'cannot be trained')
            if save_trained:
                classifier.save()

    def load_data(self):
        db = DB(settings.TOP_500_MOVIE_REVIEWS)
        reviews = get_reviews(db=db)

        feature_finder = MostCommonWordsFinder.load('top500reviews.featureset')

        def pred(review):
            return review['sentiment'] == SentimentEnum.GOOD

        partitioner = DistributionPartitioner(reviews, pred=pred, ratio=0.85)
        partitioner.partition()

        self.train_data = get_labeled_review_data(
            partitioner.training_data,
            feature_finder=feature_finder.find_features,
        )
        self.test_data = get_labeled_review_data(
            partitioner.test_data,
            feature_finder=feature_finder.find_features,
        )

    def compare(self):
        data = []
        header = ['Classifier', 'Accuracy']
        data.append(header)
        for classifier in self.classifiers:
            try:
                accuracy = nltk.classify.accuracy(classifier, self.test_data)
                data.append([classifier.name, '{:.4f}'.format(accuracy)])
            except Exception as e:
                print(classifier.name, 'failed')
        tbl = SingleTable(data)
        print(tbl.table)
