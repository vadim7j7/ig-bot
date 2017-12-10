from tornado.ioloop import IOLoop
from tornado.queues import Queue

from bot.bot import Bot


queue = Queue()


class Launch(object):
    def __init__(self, users: list = ()):
        self.users = users

    def run(self):
        IOLoop.current().run_sync(self.load)

    async def load(self):
        IOLoop.current().spawn_callback(self.consumer)
        await self.producer()
        await queue.join()

    async def producer(self):
        for user in self.users:
            await queue.put(user)

    @staticmethod
    async def consumer():
        while True:
            user = await queue.get()

            try:
                bot = Bot(user=user)
                await bot.start()
            finally:
                queue.task_done()
