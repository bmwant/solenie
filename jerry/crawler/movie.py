from urllib.parse import urljoin

from jerry.crawler.base import BaseCrawler


class MovieCrawler(BaseCrawler):
    def _build_next_page_url(self, page_num: int) -> str:
        path = f'page/{page_num}/'
        return urljoin(self.entry_url, path)
