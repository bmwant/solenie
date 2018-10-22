import settings
from buttworld.logger import get_logger
from jerry.parser.review import SentimentEnum
from summer.stats import get_text_for_reviews
from summer.generator import SimpleMarkovGenerator
from store import DB, get_reviews_by_sentiment


logger = get_logger(__name__)


def generate_reviews():
    db = DB(settings.TOP_500_MOVIE_REVIEWS)
    gen = SimpleMarkovGenerator()
    sentiments = (
        SentimentEnum.GOOD,
        SentimentEnum.NEUTRAL,
        SentimentEnum.BAD,
    )
    for sentiment in sentiments:
        reviews = get_reviews_by_sentiment(sentiment, db=db)
        text = get_text_for_reviews(reviews)
        gen.initialize_sentiment(sentiment, text)

    print('Good review:')
    print(gen.create_good_review())
    print('Neutral review:')
    print(gen.create_neutral_review())
    print('Bad review:')
    print(gen.create_bad_review())


if __name__ == '__main__':
    generate_reviews()
