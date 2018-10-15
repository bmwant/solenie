from aiohttp import ClientSession
from async_timeout import timeout


class Fetcher(object):
    def __init__(self):
        pass

    async def get(self, url, proxy='http://89.29.100.94:36976/', timeout_sec=None):
        async with timeout(timeout_sec):
            async with ClientSession() as session:
                async with session.get(url, proxy=proxy) as response:
                    return await response.text()
