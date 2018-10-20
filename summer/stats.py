import matplotlib.pyplot as plt
from wordcloud import WordCloud
from tinydb import TinyDB, Query

import settings
from buttworld.logger import get_logger
from jerry.parser.review import SentimentEnum


db = TinyDB(settings.TOP_500_MOVIE_REVIEWS)
logger = get_logger(__name__)


def get_reviews_by_sentiment(sentiment):
    query = Query()
    return db.search(query.sentiment == sentiment)


def get_text_for_reviews(reviews):
    return ' '.join([r['text'] for r in reviews])


def generate_cloud_for_text(text):
    # Generate a word cloud image
    wordcloud = WordCloud().generate(text)

    # lower max_font_size
    wordcloud = WordCloud(max_font_size=40).generate(text)
    plt.figure()
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

    # The pil way (if you don't have matplotlib)
    # image = wordcloud.to_image()
    # image.show()


def main():
    pos_reviews = get_reviews_by_sentiment(SentimentEnum.GOOD)
    reg_reviews = get_reviews_by_sentiment(SentimentEnum.NEUTRAL)
    bad_reviews = get_reviews_by_sentiment(SentimentEnum.BAD)

    pos_text = get_text_for_reviews(pos_reviews)
    reg_text = get_text_for_reviews(reg_reviews)
    bad_text = get_text_for_reviews(bad_reviews)

    generate_cloud_for_text(pos_text)
    generate_cloud_for_text(reg_text)
    generate_cloud_for_text(bad_text)


if __name__ == '__main__':
    main()
