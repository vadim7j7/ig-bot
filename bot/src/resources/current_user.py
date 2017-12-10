from bot.src.resources.feed import full_feed


async def info() -> (None, dict):
    data = await full_feed()

    if data.get('graphql') is None and data['graphql'].get('user') is None:
        return None

    user = data['graphql']['user']

    return {
        'id': user.get('id'),
        'profile_pic_url': user.get('profile_pic_url'),
        'username': user.get('username'),
    }
