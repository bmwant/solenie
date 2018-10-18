import asyncio
from random import shuffle
from http import HTTPStatus
from urllib.parse import urlparse

from aiohttp import ClientSession

from jerry.proxy import Proxy, BaseProxyPool


SCYLLA_SERVICE_URL = 'http://localhost:8899/api/v1/proxies'


class ScyllaProxyPool(BaseProxyPool):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def _check_proxy(self, proxy_url):
        return True

    def load_proxies(self):
        return asyncio.run(self._load_proxies())

    def _build_proxies_from_response(self, data):
        result = []
        for item in data:
            result.append(Proxy())

        shuffle(result)
        return result

    async def _load_proxies(self):
        scylla_url = 'https=true'
        async with ClientSession() as session:
            async with session.get(scylla_url) as response:
                data = await response.json()
                return self._build_proxies_from_response(data['proxies'])
