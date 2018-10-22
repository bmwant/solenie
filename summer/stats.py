import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk.probability import FreqDist
from nltk.tokenize import sent_tokenize, word_tokenize
from tinydb import TinyDB, Query

import settings
from buttworld.logger import get_logger
from jerry.parser.review import SentimentEnum


db = TinyDB(settings.TOP_500_MOVIE_REVIEWS)
logger = get_logger(__name__)


def get_reviews_by_sentiment(sentiment):
    query = Query()
    result = db.search(query.sentiment == sentiment)
    logger.info('Loaded %s records for %s sentiment', len(result), sentiment)
    return result


def tokenize(text):
    words = []
    for sentence in sent_tokenize(text):
        for word in word_tokenize(sentence):
            words.append(word)
    return words


def show_stats_for_text(text):
    words = [w.lower() for w in tokenize(text)]
    fd = FreqDist(words)
    logger.info('Total words: %s', len(words))
    logger.info('Recurrent words: %s', fd.B())
    logger.info('Most common words')
    for word, count in fd.most_common(20):
        logger.info('%s\t%s', word, count)


def get_text_for_reviews(reviews):
    text = ' '.join([r['text'] for r in reviews])
    show_stats_for_text(text)
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


def generate_cloud_for_text(text, name='file'):
    wordcloud = WordCloud(max_font_size=40).generate(text)

    # _pltshow(wordcloud, name)
    # The pil way (if you don't have matplotlib)
    image = wordcloud.to_image()
    # image.show()
    image.save(f'{name}.png')


# todo: stopwords
# todo: punctuations, check simple example
# ~/nltk_data/tokenizers/punkt
# https://stackoverflow.com/questions/21160310/training-data-format-for-nltk-punkt
def main():
    sentiments = (
        SentimentEnum.GOOD,
        SentimentEnum.NEUTRAL,
        SentimentEnum.BAD,
    )
    for sentiment in sentiments:
        reviews = get_reviews_by_sentiment(sentiment)
        text = get_text_for_reviews(reviews)
        generate_cloud_for_text(text, name=sentiment.name.lower())


if __name__ == '__main__':
    main()
