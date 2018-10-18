import asyncio

from buttworld.logger import get_logger
from buttworld.utils import get_base_url
from jerry.crawler import MovieCrawler, ReviewCrawler
from jerry.fetcher import Fetcher
from jerry.parser import MovieParser, ReviewParser
from jerry.proxy_pool import ProxyPool
from beth.task_manager import TaskManager
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
    # todo: add retries
    movie_page_urls = await mc.process()

    parser = ReviewParser(base_url=base_url)
    tm = TaskManager(max_retires=20)
    tasks = []
    for url in movie_page_urls[:5]:
        proxy_pool = ProxyPool()
        fetcher = Fetcher(proxy_pool=proxy_pool)
        fetcher.timeout = 20
        crawler = ReviewCrawler(entry_url=url, parser=parser, fetcher=fetcher)
        tasks.append(crawler)

    tm.add_tasks(tasks)
    await tm.process()
    reviews = tm.results
    logger.debug('Inserting %s reviews...', len(reviews))
    import pdb; pdb.set_trace()
    print(reviews)


if __name__ == '__main__':
    asyncio.run(main())
