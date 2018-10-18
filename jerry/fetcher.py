import async_timeout
from aiohttp import ClientSession

from buttworld.logger import get_logger


logger = get_logger(__name__)


class Fetcher(object):
    def __init__(self, proxy_pool=None, timeout_sec=None):
        self.proxy_pool = proxy_pool
        self.timeout_sec = timeout_sec

    @property
    def timeout(self):
        return self.timeout_sec

    @timeout.setter
    def timeout(self, value):
        self.timeout_sec = value

    async def get(self, url, timeout_sec=None):
        proxy = None
        if self.proxy_pool is not None:
            proxy = await self.proxy_pool.get_proxy()
            logger.debug('Using proxy %s', proxy)

        timeout = timeout_sec or self.timeout
        async with async_timeout.timeout(timeout):
            async with ClientSession() as session:
                logger.debug('Requesting %s', url)
                async with session.get(url, proxy=proxy) as response:
                    return await response.text()
