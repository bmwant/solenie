"""
* aiohttp.client_exceptions.ClientHttpProxyError: 500, message='Internal Server Error'
* aiohttp.client_exceptions.ClientProxyConnectionError: Cannot connect to host 78.159.79.245:57107
  ssl:None [Connect call failed ('78.159.79.245', 57107)]

* <asyncio.sslproto.SSLProtocol object at 0x7f3afe19b4a8> stalled during handshake
Traceback (most recent call last):
  File "grab_data.py", line 39, in <module>
    loop.run_until_complete(main())
  File "/usr/local/lib/python3.7/asyncio/base_events.py", line 566, in run_until_complete
    return future.result()
  File "grab_data.py", line 30, in main
    reviews = list(chain.from_iterable(await asyncio.gather(*tasks)))
  File "/usr/local/lib/python3.7/asyncio/tasks.py", line 570, in _wrap_awaitable
    return (yield from awaitable.__await__())
  File "/home/user/.pr/solenie/jerry/crawler/base.py", line 32, in process
    async for page in self.get_next_page():
  File "/home/user/.pr/solenie/jerry/crawler/base.py", line 18, in get_next_page
    page_html = await self.fetcher.get(url)
  File "/home/user/.pr/solenie/jerry/fetcher.py", line 12, in get
    async with session.get(url, proxy=proxy) as response:
  File "/home/user/.virtualenvs/solenie/lib/python3.7/site-packages/aiohttp/client.py", line 855, in __aenter__
    self._resp = await self._coro
  File "/home/user/.virtualenvs/solenie/lib/python3.7/site-packages/aiohttp/client.py", line 377, in _request
    tcp_nodelay(conn.transport, True)
  File "/home/user/.virtualenvs/solenie/lib/python3.7/site-packages/aiohttp/tcp_helpers.py", line 32, in tcp_nodelay
    sock = transport.get_extra_info('socket')
AttributeError: 'NoneType' object has no attribute 'get_extra_info'
"""
import itertools
from http import HTTPStatus
from urllib.parse import urlparse

import yaml
import aiohttp

import settings
from buttworld.logger import get_logger
from jerry.proxy import Proxy


logger = get_logger(__name__)

DEFAULT_CHECK_URL = 'http://checkip.amazonaws.com/'


async def _check_response_patch(self, resp, proxy_url):
    text = await resp.text()
    result = proxy_url in text
    if not result:
        logger.debug('%s: %s', resp.status, text)
    return result


class ProxyPool(object):
    def __init__(self, check_url: str=DEFAULT_CHECK_URL):
        self.check_url = check_url
        self._proxies = None

    @property
    def proxies(self):
        if self._proxies is None:
            self._proxies = self.load_proxies()
        return self._proxies

    async def __anext__(self):
        for proxy_url in itertools.chain(self.proxies):
            if await self._check_proxy(proxy_url):
                yield proxy_url

    async def _check_proxy(self, proxy_url):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.check_url, proxy=proxy_url) as resp:
                return await self._check_response(resp, proxy_url)

    async def _check_response(self, resp,  proxy_url) -> bool:
        text = await resp.text()
        netloc = urlparse(proxy_url).netloc
        ip, colon, port = netloc.partition(':')
        return resp.status == HTTPStatus.OK and ip in text

    def __aiter__(self):
        return self.__anext__()

    async def get_proxy(self):
        it = self.__aiter__()
        return await it.__anext__()

    def load_proxies(self):
        with open(settings.PROXIES_STORAGE_FILEPATH) as f:
            return [Proxy(**data) for data in yaml.load(f)]
