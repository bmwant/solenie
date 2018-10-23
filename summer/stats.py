import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk.probability import FreqDist


import settings
from buttworld.logger import get_logger
from jerry.parser.review import SentimentEnum
from summer.tokenizer import tokenize
from store import DB, get_reviews_by_sentiment


db = DB(settings.TOP_500_MOVIE_REVIEWS)
logger = get_logger(__name__)


def show_stats_for_text(text):
    words = tokenize(text, clean=True)
    fd = FreqDist(words)
    logger.info('Total words: %s', len(words))
    logger.info('Recurrent words: %s', fd.B())
    logger.info('Most common words')
    for word, count in fd.most_common(20):
        logger.info('%s\t%s', word, count)


def get_text_for_reviews(reviews) -> str:
    text = ' '.join([r['text'] for r in reviews])
    return text


def _pltshow(wordcloud, name=None):
    fig = plt.figure(frameon=False)
    fig.subplots_adjust(
        left=0,
        bottom=0,
        right=1,
        top=1,
        wspace=0,
        hspace=0,
    )
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    if name is None:
        plt.show()
    else:
        fig.savefig(
            f'{name}.png',
            dpi='figure',
            bbox_inches='tight',  # check
            pad_inches=0,  # these
        )


def generate_cloud_for_text(text, name=None):
    wordcloud = WordCloud(max_font_size=40).generate(text)

    # _pltshow(wordcloud, name)
    # The pil way (if you don't have matplotlib)
    image = wordcloud.to_image()
    if name is None:
        image.show()
    else:
        image.save(f'{name}.png')


# ~/nltk_data/tokenizers/punkt
# https://stackoverflow.com/questions/21160310/training-data-format-for-nltk-punkt
def main():
    sentiments = (
        SentimentEnum.GOOD,
        SentimentEnum.NEUTRAL,
        SentimentEnum.BAD,
    )
    for sentiment in sentiments:
        reviews = get_reviews_by_sentiment(sentiment, db=db)
        text = get_text_for_reviews(reviews)
        show_stats_for_text(text)
        # generate_cloud_for_text(text, name=sentiment.name.lower())


if __name__ == '__main__':
    main()
