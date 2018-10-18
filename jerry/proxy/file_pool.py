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
from http import HTTPStatus
from urllib.parse import urlparse

import yaml
import aiohttp
from aiohttp import client_exceptions

import settings
from jerry.proxy import Proxy
from jerry.proxy import BaseProxyPool


__all__ = ('FileProxyPool',)


class FileProxyPool(BaseProxyPool):
    async def init(self):
        pass

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
            self.logger.error('Failed proxy check: %s', e)
            return False

    async def _check_response(self, resp,  proxy_url) -> bool:
        text = await resp.text()
        netloc = urlparse(proxy_url).netloc
        ip, colon, port = netloc.partition(':')
        return resp.status == HTTPStatus.OK and ip in text

    def load_proxies(self):
        with open(settings.PROXIES_STORAGE_FILEPATH) as f:
            data = yaml.load(f)
            self.logger.info('Loaded %s proxies', len(data))
            return [Proxy(**d) for d in data]
