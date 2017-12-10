from bot.launch import Launch
from bot.src.structures import User, Action


def generate_users() -> list:
    action_like = Action()
    action_like.action = 'like'
    action_like.config = {}

    action_follow = Action()
    action_like.action = 'follow'
    action_like.config = {}

    user = User()
    user.id = 1
    user.credentials.email = 'LOGIN'
    user.credentials.password = 'PASSWORD'
    user.actions = [action_like, action_follow, ]

    return [user, ]


if __name__ == '__main__':
    users = generate_users()
    launch = Launch(users=users)

    launch.run()
