from bot.launch import Launch
from bot.src.structures import User


def generate_users() -> list:
    user = User()
    user.id = 1
    user.credentials.email = 'LOGIN'
    user.credentials.password = 'PASSWORD'

    user.action_get_media.params.update({
        'tags': ['develop', 'python', 'django', 'ruby on rails', 'ruby', 'reactJs', ]
    })

    return [user, ]


if __name__ == '__main__':
    users = generate_users()
    launch = Launch(users=users)

    launch.run()
