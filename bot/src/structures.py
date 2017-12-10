class Credentials(object):
    email = ''
    password = ''


class Action(object):
    action = ''
    params = {}
    config = {}
    thread_name = 'default'
    pause = {'from': 1000, 'to': 3000}


class User(object):
    id = None
    credentials = Credentials
    actions = list
