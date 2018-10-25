from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB, BernoulliNB

from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC



def main():
    import nltk
    from summer.classifier.naive_bayes import get_labeled_review_data
    from summer.partitioner import DistributionPartitioner
    from summer.features import MostCommonWordsFinder
    from froppyland.enums import SentimentEnum
    from store import DB, get_reviews
    import settings

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

    # Classifiers
    # MNB_classifier = SklearnClassifier(MultinomialNB())
    # MNB_classifier.train(train_data)
    # print('MNB_classifier accuracy percent:',
    #       nltk.classify.accuracy(MNB_classifier, test_data))
    #
    # BNB_classifier = SklearnClassifier(BernoulliNB())
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

    # Nu-Support Vector Classification
    classifier = NuSVC(nu=0.8, gamma='auto')
    NuSVC_classifier = SklearnClassifier(classifier)
    NuSVC_classifier.train(train_data)
    print("NuSVC_classifier accuracy percent:",
          nltk.classify.accuracy(NuSVC_classifier, test_data))


if __name__ == '__main__':
    main()
