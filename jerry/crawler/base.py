from itertools import count

from buttworld.logger import get_logger


class BaseCrawler(object):
    def __init__(self, entry_url, *, fetcher=None, parser=None):
        self.entry_url = entry_url
        self.fetcher = fetcher
        self.parser = parser
        self.logger = get_logger(self.__class__.__name__.lower())

    async def get_next_page(self):
        for page_num in count(start=1):
            url = self._build_next_page_url(page_num)
            self.logger.debug('Processing %s...', url)
            page_html = await self.fetcher.get(url)
            if self.parser.check(page_html):
                yield page_html
            else:
                break

    def __await__(self):
        return self.process()

    def _build_next_page_url(self, page_num: int) -> str:
        pass

    async def process(self) -> list:
        result = []
        async for page in self.get_next_page():
            result.extend(self.parser.process_page(page))
        return result
