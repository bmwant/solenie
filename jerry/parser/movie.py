from bs4 import BeautifulSoup

from jerry.parser.base import BaseParser


class MovieParser(BaseParser):
    def check(self, html: str) -> bool:
        soup = BeautifulSoup(html, 'html5lib')
        review = soup.find('div', 'reviewItem')
        if review is None:
            return False
        return True
