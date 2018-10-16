import asyncio

from buttworld.utils import get_base_url
from jerry.crawler import MovieCrawler, ReviewCrawler
from jerry.fetcher import Fetcher
from jerry.parser import MovieParser, ReviewParser


async def main():
    # Kinopoisk TOP 500 movies
    list_url = 'https://www.kinopoisk.ru/top/lists/1/filtr/all/sort/order/perpage/200/'
    base_url = get_base_url(list_url)
    # mf = Fetcher()
    # mp = MovieParser(base_url=base_url)
    # mc = MovieCrawler(entry_url=list_url, fetcher=mf, parser=mp)
    # movie_page_urls = await mc.process()
    movie_page_urls = ['https://www.kinopoisk.ru/film/723/']

    rf = Fetcher()
    rp = ReviewParser(base_url=base_url)
    tasks = [
        ReviewCrawler(entry_url=url, fetcher=rf, parser=rp)
        for url in movie_page_urls
    ]
    reviews = await asyncio.gather(*tasks)
    print(reviews)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
