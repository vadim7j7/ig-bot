import time
import random

from bot.src.user_session import UserSession
from bot.src.structures import User
from bot.src.resources import current_user, media


PAUSE_FOR_NEW_ITER = [3000, 5000]


class Bot(object):
    """
    >> bot = Bot(user: user)
    >> await bot.start()
    """

    def __init__(self, user: User):
        self.user = user
        self.run = True
        self.media = []

    async def start(self):
        user_session = UserSession(self.user.credentials)
        user_session.init_session()

        # login
        result = await user_session.login()
        if not result:
            # TODO here i need to make to send an error to a user
            return

        # Get small info about the current user
        data = await current_user.info()
        if data is not None:
            # TODO here i need to make an action for send to a user
            pass

        # Start loop:
        await self.run_loop()

    async def run_loop(self):
        """ Find -> Like -> Follow -> Unfollow -> Comment -> : """

        while self.run:
            if len(self.media) == 0:
                await self.get_media_by_tag()

            pause = random.randint(PAUSE_FOR_NEW_ITER[0], PAUSE_FOR_NEW_ITER[0]) / 1000
            time.sleep(pause)

            break

    async def get_media_by_tag(self):
        tags = self.user.action_get_media.params.get('tags')
        if tags is None:
            return None

        random.shuffle(tags)

        tag = random.choice(tags)
        data = await media.get_by(tag=tag)
        if data is None:
            return None

        self.media = data['tag']['media']['nodes']
