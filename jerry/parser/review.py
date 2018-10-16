from enum import IntEnum
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from jerry.parser.base import BaseParser


class SentimentEnum(IntEnum):
    BAD = -1
    NEUTRAL = 0
    GOOD = 1


class ReviewParser(BaseParser):
    def check(self, html: str) -> bool:
        soup = BeautifulSoup(html, 'html5lib')
        review = soup.find('div', 'reviewItem')
        if review is None:
            return False
        return True

    def process_page(self, html):
        soup = BeautifulSoup(html, 'html5lib')
        reviews = soup.find_all('div', 'reviewItem')
        for item in reviews:
            review_div = item.find('div', 'brand_words')
            review_span = review_div.find('p').find('span')
            [br.extract() for br in review_span.find_all('br')]
            review_title = self.prettify(item.find('p', 'sub_title').text)
            review_text = self.prettify(review_span.text)
            sentiment = self._get_sentiment(item)
            link_tag = item.find('p', 'links').find('a')
            link = self._get_link(link_tag)
            return {

            }

    def _get_link(self, link_tag):
        return urljoin(self.base_url, link_tag['href'])

    def _get_sentiment(self, review_item):
        response_div = review_item.find('div', 'response')
        classes = response_div.attrs['class']
        for class_ in classes:
            if class_ == 'good':
                return SentimentEnum.GOOD
            elif class_ == 'bad':
                return SentimentEnum.BAD
        return SentimentEnum.NEUTRAL
