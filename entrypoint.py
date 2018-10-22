import settings
from buttworld.logger import get_logger
from jerry.parser.review import SentimentEnum
from summer.stats import get_text_for_reviews
from summer.generator import SimpleMarkovGenerator, MarkovifyReviewGenerator
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


if __name__ == '__main__':
    generate_simple_markov_reviews()
    generate_markovify_reviews()
