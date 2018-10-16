from urllib.parse import urlparse, urlunsplit


def get_base_url(url):
    parts = urlparse(url)
    return urlunsplit((parts.scheme, parts.netloc, '', '', ''))
