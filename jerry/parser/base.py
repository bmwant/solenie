from abc import ABC, abstractmethod
from urllib.parse import urljoin
from html.entities import name2codepoint


class BaseParser(ABC):
    def __init__(self, base_url: str):
        self.base_url = base_url

    def check(self, html: str) -> bool:
        return False

    @abstractmethod
    def process_page(self, html: str):
        pass

    @staticmethod
    def prettify(string):
        nbsp_codepoint = name2codepoint['nbsp']
        nbsp_char = chr(nbsp_codepoint)

        def _prettify(_string):
            lines = _string.replace(nbsp_char, ' ').strip().splitlines()
            return ' '.join(lines)

        return _prettify(string)

    def _get_link(self, link_tag):
        return urljoin(self.base_url, link_tag['href'])
