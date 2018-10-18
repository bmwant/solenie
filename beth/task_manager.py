import asyncio

from buttworld.logger import get_logger


class TaskManager(object):
    def __init__(self, max_retires=None):
        self.max_retries = max_retires
        self.tasks = []
        self.results = []
        self.logger = get_logger(self.__class__.__name__.lower())

    def add_tasks(self, tasks):
        [self.tasks.append(task) for task in tasks]

    async def process(self):
        retries = 0
        while self.tasks:
            self.logger.info('Total tasks %s', len(self.tasks))
            tasks = self.tasks[:]
            failed = []
            self.logger.info('Iteration %s', retries)
            results = await asyncio.gather(*tasks, return_exceptions=True)

            self.logger.info('Gathered results %s', results)
            for task, res in zip(tasks, results):
                if isinstance(res, Exception):
                    self.logger.error('Task failed: %s', res)
                    failed.append(task)
                else:
                    if not res:
                        self.logger.error('Empty result %s', task)
                    self.results.append(res)
            del self.tasks
            self.tasks = failed
            retries += 1
            if self.max_retries is not None and retries > self.max_retries:
                self.logger.error(
                    'Cannot complete all tasks. Exceeded retries limit: %s',
                    self.max_retries
                )
                return

        self.logger.info('Finished %s tasks. Retries: %s.',
                         len(self.results), retries)


class Crawler(object):
    def __init__(self, c=0, *args, **kwargs):
        self.c = c

    async def process(self):
        self.c += 1
        if self.c == 1:
            raise RuntimeError('error')
        return self.c

    def __await__(self):
        return self.process().__await__()

    def task(self):
        return asyncio.create_task(self.process())


async def main():
    # Create a queue that we will use to store our "workload".
    queue = asyncio.Queue()
    tm = TaskManager()
    c1 = Crawler(c=3)
    t1 = c1.task()
    print(await t1)
    c2 = Crawler()
    c3 = Crawler()

    # tm.add_tasks([c1, c2, c3])
    # await tm.process()
    # print(tm.results)


if __name__ == '__main__':
    asyncio.run(main())
