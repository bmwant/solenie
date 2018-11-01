import nltk

from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.svm import NuSVC

import settings
from store import DB, get_reviews
from froppyland.enums import SentimentEnum
from summer.features import MostCommonWordsFinder
from summer.partitioner import DistributionPartitioner
from summer.classifier.naive_bayes import get_labeled_review_data


def main():
    db = DB(settings.TOP_500_MOVIE_REVIEWS)
    reviews = get_reviews(db=db)
    feature_finder = MostCommonWordsFinder.load('top500reviews.featureset')

    def pred(review):
        return review['sentiment'] == SentimentEnum.GOOD

    partitioner = DistributionPartitioner(reviews, pred=pred, ratio=0.85)
    partitioner.partition()

    train_data = get_labeled_review_data(
        partitioner.training_data,
        feature_finder.find_features,
    )
    test_data = get_labeled_review_data(
        partitioner.test_data,
        feature_finder.find_features,
    )
    # Nu-Support Vector Classification
    # nu 0.01-0.05 to work
    classifier = NuSVC(nu=0.04, gamma='auto')
    # 0.8547
    NuSVC_classifier = SklearnClassifier(classifier)
    NuSVC_classifier.train(train_data)
    print("NuSVC_classifier accuracy percent:",
          nltk.classify.accuracy(NuSVC_classifier, test_data))


if __name__ == '__main__':
    main()
