from bs4 import BeautifulSoup

from jerry.parser.base import BaseParser
from froppyland.enums import SentimentEnum
from store import Review


class ReviewParser(BaseParser):
    def check(self, html: str) -> bool:
        soup = BeautifulSoup(html, 'html5lib')
        review = soup.find('div', 'reviewItem')
        if review is None:
            return False
        return True

    def process_page(self, html) -> list:
        soup = BeautifulSoup(html, 'html5lib')
        reviews = soup.find_all('div', 'reviewItem')
        result = []
        for item in reviews:
            review_div = item.find('div', 'brand_words')
            review_span = review_div.find('p').find('span')
            [br.extract() for br in review_span.find_all('br')]
            review_title = self.prettify(item.find('p', 'sub_title').text)
            review_text = self.prettify(review_span.text)
            sentiment = self._get_sentiment(item)
            link_tag = item.find('p', 'links').find('a')
            link = self._get_link(link_tag)
            review = Review(
                title=review_title,
                text=review_text,
                sentiment=sentiment,
                link=link,
            )
            result.append(review)
        return result

    def _get_sentiment(self, review_item):
        response_div = review_item.find('div', 'response')
        classes = response_div.attrs['class']
        for class_ in classes:
            if class_ == 'good':
                return SentimentEnum.GOOD
            elif class_ == 'bad':
                return SentimentEnum.BAD
        return SentimentEnum.NEUTRAL
