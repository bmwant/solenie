import asyncio
from itertools import chain

from buttworld.logger import get_logger
from buttworld.utils import get_base_url
from jerry.crawler import MovieCrawler, ReviewCrawler
from jerry.fetcher import Fetcher
from jerry.parser import MovieParser, ReviewParser
from jerry.proxy_pool import ProxyPool
from store import insert_review


logger = get_logger(__name__)


async def main():
    # Kinopoisk TOP 500 movies
    list_url = (
        'https://www.kinopoisk.ru/'
        'top/lists/1/filtr/all/sort/order/perpage/200/'
    )
    base_url = get_base_url(list_url)
    proxy_pool = ProxyPool()
    mf = Fetcher(proxy_pool=proxy_pool)
    mp = MovieParser(base_url=base_url)
    mc = MovieCrawler(entry_url=list_url, fetcher=mf, parser=mp)
    movie_page_urls = await mc.process()

    rf = Fetcher(proxy_pool=proxy_pool)
    rp = ReviewParser(base_url=base_url)
    tasks = [
        ReviewCrawler(entry_url=url, fetcher=rf, parser=rp)
        for url in movie_page_urls
    ]
    reviews = list(chain.from_iterable(await asyncio.gather(*tasks)))
    logger.debug('Inserting %s reviews...', len(reviews))

    for r in reviews:
        insert_review(r)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
