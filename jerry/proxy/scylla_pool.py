from random import shuffle

from aiohttp import ClientSession

from jerry.proxy import Proxy, BaseProxyPool


__all__ = ('ScyllaProxyPool',)

SCYLLA_SERVICE_URL = 'http://localhost:8899/api/v1/proxies'


class ScyllaProxyPool(BaseProxyPool):
    def __init__(self, *args, scylla_url=SCYLLA_SERVICE_URL, **kwargs):
        self.scylla_url = scylla_url
        super().__init__(*args, **kwargs)

    async def _check_proxy(self, proxy_url):
        return True

    async def init(self):
        proxies = await self._load_proxies()
        self.logger.info('Loaded %s proxies', len(proxies))
        type(self)._proxies = proxies

    def load_proxies(self):
        if type(self)._proxies is None:
            self.logger.warning('You forgot to call init method!')

    def _build_proxies_from_response(self, data) -> list:
        result = []
        for item in data:
            if item['country'] == 'UA':
                continue
            ip = item['ip']
            port = item['port']
            url = f'http://{ip}:{port}/'
            result.append(Proxy(url=url))

        return result

    async def _load_proxies(self):
        params = {'https': 'true'}
        async with ClientSession() as session:
            async with session.get(self.scylla_url, params=params) as response:
                data = await response.json()
                return self._build_proxies_from_response(data['proxies'])
