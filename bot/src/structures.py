class Credentials(object):
    email: str = None
    password: str = None


class Action(object):
    name: str = None
    allow: bool = True
    params: dict = {}
    config: dict = {'delay': {'from': 1000, 'to': 3000}}
    data: object = None

    def __init__(self, name: str):
        self.name = name


class User(object):
    id: int = None
    credentials: Credentials = Credentials()
    action_get_media: Action = Action(name='get_media')
    action_like: Action = Action(name='like')
    action_follow: Action = Action(name='follow')
    action_unfollow: Action = Action(name='unfollow')
    action_comment: Action = Action(name='comment')
