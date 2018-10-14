from enum import IntEnum
from urllib.parse import urljoin
from html.entities import name2codepoint
from bs4 import BeautifulSoup

from store import insert_review


base_url = 'https://www.kinopoisk.ru'


class SentimentEnum(IntEnum):
    BAD = -1
    NEUTRAL = 0
    GOOD = 1


def prettify(string):
    nbsp_codepoint = name2codepoint['nbsp']
    nbsp_char = chr(nbsp_codepoint)

    def _prettify(_string):
        lines = _string.replace(nbsp_char, ' ').strip().splitlines()
        return ' '.join(lines)

    return _prettify(string)


def get_url(link_tag):
    return urljoin(base_url, link_tag['href'])


def get_sentiment(review_item):
    response_div = review_item.find('div', 'response')
    classes = response_div.attrs['class']
    for class_ in classes:
        if class_ == 'good':
            return SentimentEnum.GOOD
        elif class_ == 'bad':
            return SentimentEnum.BAD
    return SentimentEnum.NEUTRAL


def process_page(html):
    soup = BeautifulSoup(html, 'html5lib')
    reviews = soup.find_all('div', 'reviewItem')
    for item in reviews:
        review_div = item.find('div', 'brand_words')
        review_span = review_div.find('p').find('span')
        [br.extract() for br in review_span.find_all('br')]
        review_title = prettify(item.find('p', 'sub_title').text)
        review_text = prettify(review_span.text)
        sentiment = get_sentiment(item)
        link = item.find('p', 'links').find('a')
        url = get_url(link)
        insert_review(review_title, review_text, sentiment, url, dry_run=True)


def main():
    with open('test.html') as f:
        process_page(f.read())


if __name__ == '__main__':
    main()
