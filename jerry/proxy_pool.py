"""
* Exception in callback SSLProtocol._process_write_backlog()
handle: <Handle SSLProtocol._process_write_backlog()>
Traceback (most recent call last):
  File "/usr/local/lib/python3.7/asyncio/sslproto.py", line 648, in _process_write_backlog
    ssldata = self._sslpipe.do_handshake(
AttributeError: 'NoneType' object has no attribute 'do_handshake'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/usr/local/lib/python3.7/asyncio/events.py", line 88, in _run
    self._context.run(self._callback, *self._args)
  File "/usr/local/lib/python3.7/asyncio/sslproto.py", line 674, in _process_write_backlog
    self._on_handshake_complete(exc)
  File "/usr/local/lib/python3.7/asyncio/sslproto.py", line 594, in _on_handshake_complete
    sslobj = self._sslpipe.ssl_object
AttributeError: 'NoneType' object has no attribute 'ssl_object'
*
"""
import asyncio
import itertools
from random import shuffle
from http import HTTPStatus
from urllib.parse import urlparse

import yaml
import aiohttp
from aiohttp import client_exceptions

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

    _proxies = None

    def __init__(self, check_url: str=DEFAULT_CHECK_URL):
        self.check_url = check_url
        self._instance_proxies = None
        self._aiter = None

    @property
    def proxies(self):
        if ProxyPool._proxies is None:
            ProxyPool._proxies = self.load_proxies()

        if self._instance_proxies is None:
            self._instance_proxies = ProxyPool._proxies[:]
            shuffle(self._instance_proxies)
        return self._instance_proxies

    async def __anext__(self):
        for proxy in itertools.cycle(self.proxies):
            if await self._check_proxy(proxy.url):
                yield proxy.url
            # don't be so fast throwing another proxy
            await asyncio.sleep(0.5)

    async def _check_proxy(self, proxy_url):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                        self.check_url, proxy=proxy_url) as resp:
                    return await self._check_response(resp, proxy_url)
        except (
            client_exceptions.ClientOSError,
            client_exceptions.ClientHttpProxyError,
            client_exceptions.ServerDisconnectedError,
            client_exceptions.ClientProxyConnectionError,
        ) as e:
            logger.error('Failed proxy check: %s', e)
            return False

    async def _check_response(self, resp,  proxy_url) -> bool:
        text = await resp.text()
        netloc = urlparse(proxy_url).netloc
        ip, colon, port = netloc.partition(':')
        return resp.status == HTTPStatus.OK and ip in text

    @property
    def __aiter(self):
        if self._aiter is None:
            self._aiter = self.__anext__()
        return self._aiter

    def __aiter__(self):
        return self.__aiter

    async def get_proxy(self):
        it = self.__aiter__()
        return await it.__anext__()

    def load_proxies(self):
        with open(settings.PROXIES_STORAGE_FILEPATH) as f:
            data = yaml.load(f)
            logger.info('Loaded %s proxies', len(data))
            return [Proxy(**d) for d in data]

    def __len__(self):
        return len(self.proxies)
