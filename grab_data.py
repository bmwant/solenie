import asyncio

from jerry.crawler import MovieCrawler, ReviewCrawler
from jerry.fetcher import Fetcher
from jerry.parser import Parser


async def main():
    # Kinopoisk TOP 500 movies
    list_url = 'https://www.kinopoisk.ru/top/lists/1/filtr/all/sort/order/perpage/200/'
    mc = MovieCrawler(entry_url=list_url)
    movie_page_urls = await mc.process()

    fetcher = Fetcher()
    parser = Parser()
    tasks = [
        ReviewCrawler(entry_url=url, fetcher=fetcher, parser=parser)
        for url in movie_page_urls
    ]
    await asyncio.gather(*tasks)



if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
