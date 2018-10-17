import asyncio
from asyncio.tasks import FIRST_EXCEPTION
from collections import deque

from buttworld.logger import get_logger


class TaskManager(object):
    def __init__(self, maxsize=0):
        self.maxsize = maxsize
        # self.queue = asyncio.Queue(maxsize=maxsize)
        self.tasks = []
        self.results = []
        self.logger = get_logger(self.__class__.__name__.lower())

    def add_tasks(self, tasks):
        [self.tasks.append(task) for task in tasks]

    async def process(self):
        retries = 0
        while self.tasks:
            tasks = self.tasks[:]
            failed = []

            results = await asyncio.gather(*tasks, return_exceptions=True)
            # import pdb; pdb.set_trace()

            for task, res in zip(self.tasks, results):
                if isinstance(res, Exception):
                    self.logger.error('Task failed: %s', res)
                    retries += 1
                    failed.append(task)
                else:
                    self.results.append(res)
            # await asyncio.sleep(3)
            del self.tasks
            self.tasks = failed

        self.logger.info('Finished %s tasks. Retries: %s.',
                         len(self.results), retries)


class Crawler(object):
    def __init__(self, c=0):
        self.c = c

    async def process(self):
        self.c += 1
        if self.c == 1:
            raise RuntimeError('error')
        return self.c

    def __await__(self):
        return self.process().__await__()



async def main():
    # Create a queue that we will use to store our "workload".
    queue = asyncio.Queue()
    tm = TaskManager()
    c1 = Crawler(c=3)
    # print(await c1)
    c2 = Crawler()
    c3 = Crawler()

    tm.add_tasks([c1, c2, c3])
    await tm.process()
    print(tm.results)


if __name__ == '__main__':
    asyncio.run(main())
