import matplotlib.pyplot as plt
from wordcloud import WordCloud
from tinydb import TinyDB, Query

import settings


db = TinyDB(settings.TOP_500_MOVIE_REVIEWS)


def main():
    query = Query()
    results = db.search(query.text.exists())[:10]
    text = results[0]['text']

    # Generate a word cloud image
    wordcloud = WordCloud().generate(text)

    # lower max_font_size
    wordcloud = WordCloud(max_font_size=40).generate(text)
    plt.figure()
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

    # The pil way (if you don't have matplotlib)
    image = wordcloud.to_image()
    image.show()


if __name__ == '__main__':
    main()
