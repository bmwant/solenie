from urllib.parse import urljoin

from jerry.crawler.base import BaseCrawler

"""
https://www.kinopoisk.ru/film/447301/ord/rating/perpage/200/page/2/#list
"""


class ReviewCrawler(BaseCrawler):
    def _build_next_page_url(self, page_num: int) -> str:
        path = f'ord/rating/perpage/200/page/{page_num}/#list'
        return urljoin(self.entry_url, path)
