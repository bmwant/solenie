import settings
from buttworld.logger import get_logger
from froppyland.enums import SentimentEnum
from beth.comparator import ClassifierComparator
from summer.stats import get_text_for_reviews
from summer.tokenizer import tokenize, F_LOWERCASE
from summer.generator import SimpleMarkovGenerator, MarkovifyReviewGenerator
from summer.partitioner import DistributionPartitioner
from summer.classifier import NaiveBayesClassifier
from summer.classifier.others import ScikitClassifierWrapper
from summer.classifier.naive_bayes import get_labeled_review_data
from summer.features import MostCommonWordsFinder
from store import DB, get_reviews, get_reviews_by_sentiment

from sklearn.naive_bayes import (
    GaussianNB,
    BernoulliNB,
    ComplementNB,
    MultinomialNB,
)
from sklearn.svm import SVC, LinearSVC, NuSVC, SVR, NuSVR
from sklearn.linear_model import (
    Perceptron,
    SGDClassifier,
    RidgeClassifier,
    LogisticRegression,
    LogisticRegressionCV,
    OrthogonalMatchingPursuit,
    PassiveAggressiveClassifier,
)


logger = get_logger(__name__)
db = DB(settings.TOP_500_MOVIE_REVIEWS)


def generate_simple_markov_reviews():
    gen = SimpleMarkovGenerator()
    sentiments = (
        SentimentEnum.GOOD,
        SentimentEnum.NEUTRAL,
        SentimentEnum.BAD,
    )
    for sentiment in sentiments:
        reviews = get_reviews_by_sentiment(sentiment, db=db)
        text = get_text_for_reviews(reviews)
        gen.initialize_model(sentiment, text)

    logger.info('Generating reviews using %s', gen)
    print('Good review:')
    print(gen.create_good_review())
    print('Neutral review:')
    print(gen.create_neutral_review())
    print('Bad review:')
    print(gen.create_bad_review())


def generate_markovify_reviews():
    gen = MarkovifyReviewGenerator()
    sentiments = (
        SentimentEnum.GOOD,
        SentimentEnum.NEUTRAL,
        SentimentEnum.BAD,
    )
    for sentiment in sentiments:
        reviews = get_reviews_by_sentiment(sentiment, db=db)
        text = get_text_for_reviews(reviews)
        gen.initialize_model(sentiment, text)

    logger.info('Generating reviews using %s', gen)
    print('Good review:')
    print(gen.create_good_review())
    print('Neutral review:')
    print(gen.create_neutral_review())
    print('Bad review:')
    print(gen.create_bad_review())


def classify_naive_bayes():
    reviews = get_reviews(db=db)
    text = get_text_for_reviews(reviews)
    logger.debug('Tokenizing text...')
    words = tokenize(text)
    feature_finder = MostCommonWordsFinder(n_words=500)
    feature_finder.process(words)
    feature_finder.save('top500reviews.featureset')

    def pred(review):
        return review['sentiment'] == SentimentEnum.GOOD

    partitioner = DistributionPartitioner(reviews, pred=pred, ratio=0.85)
    partitioner.partition()
    classifier = NaiveBayesClassifier()
    logger.debug('Labeling training data...')
    train_data = get_labeled_review_data(
        partitioner.training_data,
        feature_finder.find_features,
    )
    test_data = get_labeled_review_data(
        partitioner.test_data,
        feature_finder.find_features,
    )
    classifier.train(train_data)
    accuracy = classifier.accuracy(test_data)
    print('Accuracy: {:.2f}'.format(accuracy*100))
    classifier.show_top_features()
    classifier.save()


def load_trained_naive_bayes_classifier():
    feature_finder = MostCommonWordsFinder.load(
        'top500reviews.featureset')
    classifier = NaiveBayesClassifier.load(
        'naivebayesclassifier_20181025.classifier')

    reviews = get_reviews_by_sentiment(SentimentEnum.BAD, db=db)
    correct = 0
    wrong = 0
    for review in reviews:
        featureset = feature_finder.find_features(
            tokenize(review['text'], clean_filter=F_LOWERCASE))
        original_sentiment = SentimentEnum(review['sentiment'])
        guessed_sentiment = SentimentEnum(classifier.classify(featureset))
        if original_sentiment == guessed_sentiment:
            correct += 1
        else:
            wrong += 1

    print('Bad correct: %s, wrong: %s' % (correct, wrong))


def compare_bayes_classifiers():
    # Bayes classifiers
    classifiers = (
        ScikitClassifierWrapper(MultinomialNB()),
        ScikitClassifierWrapper(BernoulliNB()),
        # ScikitClassifierWrapper(GaussianNB()),
        ScikitClassifierWrapper(ComplementNB()),
    )
    # c = ScikitClassifierWrapper.load('multinomialnb_20181101.classifier')
    # cc = ClassifierComparator(classifiers=[c])
    cc = ClassifierComparator(classifiers=classifiers)
    cc.load_data()

    cc.train_classifiers()
    cc.compare()


def compare_support_vector_classifiers():
    classifiers = (
        ScikitClassifierWrapper(SVC(gamma='scale')),
        ScikitClassifierWrapper(NuSVC(nu=0.04, gamma='scale')),
        # ScikitClassifierWrapper(SVR(gamma='scale')),
        # ScikitClassifierWrapper(NuSVR(gamma='scale')),
        ScikitClassifierWrapper(LinearSVC()),
    )
    cc = ClassifierComparator(classifiers=classifiers)
    cc.load_data()

    cc.train_classifiers()
    cc.compare()


def compare_linear_classifiers():
    # No way
    # Lars
    # LassoLars
    # Lasso
    # ElasticNet
    # HuberRegressor
    # Hinge
    # SGDRegressor
    # Ridge
    # RANSACRegressor
    # TheilSenRegressor

    classifiers = (
        # ScikitClassifierWrapper(ElasticNetCV(cv=5, eps=0.01)),

        ScikitClassifierWrapper(SGDClassifier(max_iter=1000, tol=0.01)),
        ScikitClassifierWrapper(LogisticRegression()),
        ScikitClassifierWrapper(RidgeClassifier()),
        ScikitClassifierWrapper(LogisticRegressionCV()),
        ScikitClassifierWrapper(OrthogonalMatchingPursuit()),
        ScikitClassifierWrapper(PassiveAggressiveClassifier()),
        ScikitClassifierWrapper(Perceptron(max_iter=1000, tol=0.01)),
    )
    cc = ClassifierComparator(classifiers=classifiers)
    cc.load_data()

    cc.train_classifiers(save_trained=False)
    cc.compare()


if __name__ == '__main__':
    # generate_simple_markov_reviews()
    # generate_markovify_reviews()
    # classify_naive_bayes()
    # load_trained_naive_bayes_classifier()
    # compare_support_vector_classifiers()
    compare_linear_classifiers()
