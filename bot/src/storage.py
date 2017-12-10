import redis
from json.decoder import JSONDecodeError

from tornado.escape import json_encode, json_decode


def connect(db: int = 0) -> redis.StrictRedis:
    return redis.StrictRedis(host='localhost', port=6379, db=db)


def save_data(key: str, data: object, db: int = 0):
    if data.__class__.__name__ == 'dict' or data.__class__.__name__ == 'list':
        connect(db).set(key, json_encode(data))
    else:
        connect(db).set(key, data)


def get_data(key: str, db: int = 0) -> (dict, str):
    result = connect(db).get(key)
    if result is None:
        return None

    try:
        return json_decode(result)
    except JSONDecodeError:
        return result


def destroy(key: str, db: int = 0):
    connect(db).delete(key)
