from unittest.mock import MagicMock


class AsyncMock(MagicMock):

    def __await__(self):
        async def coro():
            return self.__call__()
        return coro().__await__()
