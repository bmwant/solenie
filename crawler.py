import asyncio
from urllib.parse import urljoin
from itertools import count
from parser import Parser
from fetcher import Fetcher

"""
https://www.kinopoisk.ru/film/447301/ord/rating/perpage/200/page/2/#list
"""


class KinopoiskCrawler(object):
    def __init__(self, movie_url, *, fetcher=None, parser=None):
        self.movie_url = movie_url
        self.fetcher = fetcher
        self.parser = parser

    async def get_next_page(self):
        for page_num in count(start=1):
            url = self._build_url(page_num)
            print('Requesting', url)
            page_html = await self.fetcher.get(url)
            if self.parser.check(page_html):
                yield page_html
            else:
                break

    def _build_url(self, page_num: int) -> str:
        path = f'ord/rating/perpage/200/page/{page_num}/#list'
        return urljoin(self.movie_url, path)

    async def process(self):
        async for page in self.get_next_page():
            self.parser.process_page(page, dry_run=True)



async def main():
    movie_url = 'https://www.kinopoisk.ru/film/447301/'
    f = Fetcher()
    p = Parser()
    kc = KinopoiskCrawler(movie_url, fetcher=f, parser=p)
    await kc.process()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
