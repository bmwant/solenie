from aiohttp import ClientSession
from async_timeout import timeout

from buttworld.logger import get_logger


logger = get_logger(__name__)


class Fetcher(object):
    def __init__(self, proxy_pool=None):
        self.proxy_pool = proxy_pool

    async def get(self, url, timeout_sec=None):
        proxy = None
        if self.proxy_pool is not None:
            proxy = await self.proxy_pool.get_proxy()
            logger.debug('Using proxy %s', proxy)

        async with timeout(timeout_sec):
            async with ClientSession() as session:
                async with session.get(url, proxy=proxy) as response:
                    return await response.text()
