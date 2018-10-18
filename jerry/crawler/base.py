from abc import ABC, abstractmethod
from itertools import count

from buttworld.logger import get_logger


class BaseCrawler(ABC):
    def __init__(self, entry_url, *, fetcher=None, parser=None):
        self.entry_url = entry_url
        self.fetcher = fetcher
        self.parser = parser
        self.logger = get_logger(self.__class__.__name__.lower())

    async def get_next_page(self):
        for page_num in count(start=1):
            url = self._build_next_page_url(page_num)
            page_html = await self.fetcher.get(url)
            if self.parser.check(page_html):
                yield page_html
            else:
                break

    def __await__(self):
        return self.process().__await__()

    @abstractmethod
    def _build_next_page_url(self, page_num: int) -> str:
        pass

    async def process(self) -> list:
        result = []
        async for page in self.get_next_page():
            data = self.parser.process_page(page)
            if not data:
                self.logger.error('No data when crawl %s', self.entry_url)
            else:
                result.extend(data)
        return result

    def __str__(self):
        return f'{self.__class__.__name__}[{self.entry_url}]'
