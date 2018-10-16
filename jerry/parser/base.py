from html.entities import name2codepoint


class BaseParser(object):
    def __init__(self, base_url: str):
        self.base_url = base_url

    def check(self, html: str) -> bool:
        return False

    def process_page(self, *args, **kwargs):
        pass

    @staticmethod
    def prettify(string):
        nbsp_codepoint = name2codepoint['nbsp']
        nbsp_char = chr(nbsp_codepoint)

        def _prettify(_string):
            lines = _string.replace(nbsp_char, ' ').strip().splitlines()
            return ' '.join(lines)

        return _prettify(string)
