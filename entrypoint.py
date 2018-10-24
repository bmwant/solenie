import random

import settings
from buttworld.logger import get_logger
from jerry.parser.review import SentimentEnum
from summer.stats import get_text_for_reviews, get_most_common_words
from summer.tokenizer import tokenize, F_LOWERCASE
from summer.generator import SimpleMarkovGenerator, MarkovifyReviewGenerator
from summer.partitioner import DistributionPartitioner
from summer.classifier import NaiveBayesClassifier
from summer.classifier.naive_bayes import get_features
from store import DB, get_reviews, get_reviews_by_sentiment


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
    def pred(review):
        return review['sentiment'] == SentimentEnum.GOOD

    partitioner = DistributionPartitioner(reviews, pred=pred, ratio=0.8)
    partitioner.partition()
    # todo (misha): save classifier
    classifier = NaiveBayesClassifier(
        partitioner.training_data,
        partitioner.test_data,
    )
    classifier.train()
    print(classifier.accuracy)
    classifier.show_top_features()

    text = get_text_for_reviews(reviews)
    word_features = get_most_common_words(text, n_words=30)
    # todo (misha): reuse
    find_features = get_features(word_features)
    # todo (misha): classify all three sentiments
    for _ in range(3):
        review = random.choice(reviews)
        featureset = find_features(
            tokenize(review['text'], clean_filter=F_LOWERCASE))
        print(classifier.classify(featureset))


if __name__ == '__main__':
    # generate_simple_markov_reviews()
    # generate_markovify_reviews()
    classify_naive_bayes()
