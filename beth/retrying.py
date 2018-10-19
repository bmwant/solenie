from functools import wraps

from buttworld.logger import get_logger


logger = get_logger(__name__)


class RetryError(Exception):
    pass


def retry(max_retries=0):
    def inner(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            retries = 1
            while True:
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    if retries > max_retries:
                        raise RetryError(e) from e
                    logger.debug('Got %s error, retrying...', e)
                    retries += 1
        return wrapper
    return inner
