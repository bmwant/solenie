import asyncio

from jerry.crawler import MovieCrawler


async def main():
    # Kinopoisk TOP 500 movies
    list_url = 'https://www.kinopoisk.ru/top/lists/1/filtr/all/sort/order/perpage/200/'
    mc = MovieCrawler(list_url=list_url)
    movie_page_urls = await mc.process()



if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
