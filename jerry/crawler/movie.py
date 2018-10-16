from urllib.parse import urljoin

from jerry.crawler.base import BaseCrawler


class MovieCrawler(BaseCrawler):

    async def get_next_page(self):
        pass

    def _build_next_page_url(self, page_num: int) -> str:
        path = 'https://www.kinopoisk.ru/top/lists/1/filtr/all/sort/order/perpage/200/'
        return urljoin(self.entry_url, path)

    async def process(self):
        pass


if __name__ == '__main__':
    mc = MovieCrawler(entry_url='http:/asdfsa')
    mc.logger.info('Thats me')
