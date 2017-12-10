from bot.src.user_session import UserSession
from bot.src.structures import User
from bot.src.resources import current_user


async def start(user: User):
    user_session = UserSession(user.credentials)
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
