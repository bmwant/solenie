from aiohttp import ClientSession
from async_timeout import timeout


class Fetcher(object):
    def __init__(self, proxy_pool=None):
        self.proxy_pool = proxy_pool

    async def get(self, url, proxy=, timeout_sec=None):
        async with timeout(timeout_sec):
            async with ClientSession() as session:
                async with session.get(url, proxy=proxy) as response:
                    return await response.text()
