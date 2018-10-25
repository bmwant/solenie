import settings
from buttworld.logger import get_logger
from jerry.parser.review import SentimentEnum
from summer.stats import get_text_for_reviews, get_most_common_words
from summer.tokenizer import tokenize, F_LOWERCASE
from summer.generator import SimpleMarkovGenerator, MarkovifyReviewGenerator
from summer.partitioner import DistributionPartitioner
from summer.classifier import NaiveBayesClassifier
from summer.classifier.naive_bayes import get_feature_finder
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
    text = get_text_for_reviews(reviews)
    logger.debug('Getting features from the whole text...')
    word_features = get_most_common_words(text, n_words=1000)
    feature_finder = get_feature_finder(word_features)

    def pred(review):
        return review['sentiment'] == SentimentEnum.GOOD

    partitioner = DistributionPartitioner(reviews, pred=pred, ratio=0.7)
    partitioner.partition()
    classifier = NaiveBayesClassifier(
        partitioner.training_data,
        partitioner.test_data,
        feature_finder=feature_finder,
    )
    classifier.train()
    print('Accuracy: {:.2f}'.format(classifier.accuracy*100))
    classifier.show_top_features()
    classifier.save()

    reviews = get_reviews_by_sentiment(SentimentEnum.BAD, db=db)
    for review in reviews:
        featureset = feature_finder(
            tokenize(review['text'], clean_filter=F_LOWERCASE))
        original_sentiment = SentimentEnum(review['sentiment'])
        guessed_sentiment = SentimentEnum(classifier.classify(featureset))
        if original_sentiment == guessed_sentiment:
            print(f'Original sentiment {original_sentiment.name}. '
                  f'Sentiment guessed: {guessed_sentiment.name}')


def load_trained_naive_bayes_classifier():
    pass


if __name__ == '__main__':
    # generate_simple_markov_reviews()
    # generate_markovify_reviews()
    classify_naive_bayes()
