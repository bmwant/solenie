import asyncio
from urllib.parse import urlparse, urlunsplit

from aiohttp import ClientSession, TCPConnector
from async_timeout import timeout


limit = 1000
url = 'https://www.kinopoisk.ru/film/939411/'

proxies = (
    '138.68.165.154:8080',
    '176.192.20.146:32231',
)


def get_base_url(url):
    parts = urlparse(url)
    return urlunsplit((parts.scheme, parts.netloc, '', '', ''))


async def fetch(url, session, proxy=None, timeout_sec=None):
    async with timeout(timeout_sec):
        async with session.get(url, proxy=proxy) as response:
            return await response.text()


async def bound_fetch(sem, url, session, proxy=None):
    # Getter function with semaphore.
    async with sem:
        await fetch(url, session, proxy=proxy)


async def fetch_parallel(session, r):
    url = "http://localhost:8080/{}"
    tasks = []
    # create instance of Semaphore
    sem = asyncio.Semaphore(limit)
    for i in range(r):
        # pass Semaphore and session to every GET request
        task = asyncio.ensure_future(bound_fetch(sem, url.format(i), session))
        tasks.append(task)
    responses = asyncio.gather(*tasks)
    await responses


async def main():
    connector = TCPConnector(limit=None)
    url = 'https://www.kinopoisk.ru/film/447301/ord/rating/perpage/200/page/4/#list'
    async with ClientSession(connector=connector) as session:
        res = await fetch(
            url,
            session,
            proxy='http://176.192.20.146:32231/',
            timeout_sec=10,
        )
        # write_data(res)
        # await fetch_parallel(session, int(sys.argv[1]))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
