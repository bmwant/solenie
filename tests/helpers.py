from unittest.mock import MagicMock


class AsyncMock(MagicMock):

    def __await__(self):
        async def coro():
            return self.__call__()
        return coro().__await__()

    # async def async_call(self):
    #     self.__call__()
