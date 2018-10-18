import asyncio
import itertools
from abc import ABC, abstractmethod
from random import shuffle

from buttworld.logger import get_logger


DEFAULT_CHECK_URL = 'http://checkip.amazonaws.com/'


class BaseProxyPool(ABC):

    _proxies = None

    def __init__(self, check_url: str=DEFAULT_CHECK_URL):
        self.check_url = check_url
        self._instance_proxies = None
        self._aiter = None
        self.logger = get_logger(self.__class__.__name__.lower())

    @property
    def proxies(self):
        class_ = self.__class__  # type(self)?
        if class_._proxies is None:
            class_._proxies = self.load_proxies()

        if self._instance_proxies is None:
            self._instance_proxies = class_._proxies[:]
            shuffle(self._instance_proxies)
        return self._instance_proxies

    async def __anext__(self):
        for proxy in itertools.cycle(self.proxies):
            if await self._check_proxy(proxy.url):
                yield proxy.url
            # don't be so fast throwing another proxy
            await asyncio.sleep(0.5)

    @abstractmethod
    async def _check_proxy(self, proxy_url: str) -> bool:
        pass

    @abstractmethod
    async def init(self):
        pass

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

    @abstractmethod
    def load_proxies(self):
        pass

    def __len__(self):
        return len(self.proxies)
