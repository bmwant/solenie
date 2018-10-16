from bs4 import BeautifulSoup

from jerry.parser.base import BaseParser


class MovieParser(BaseParser):
    def check(self, html: str) -> bool:
        soup = BeautifulSoup(html, 'html5lib')
        items_table = soup.find('table', {'id': 'itemList'})
        td_tags = items_table.find_all('td')
        return len(td_tags) > 1

    def process_page(self, html):
        soup = BeautifulSoup(html, 'html5lib')
        items_table = soup.find('table', {'id': 'itemList'})
        movie_urls = items_table.find_all('a', 'all')
        return [self._get_link(tag) for tag in movie_urls]
