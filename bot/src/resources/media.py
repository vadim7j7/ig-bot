from tornado.escape import json_decode

from bot.src.urls import URL_GET_BY_TAG
from bot.src.client import Client


async def get_by(tag: str):
    url = URL_GET_BY_TAG.format(tag=tag)

    response = await Client.send_request(url)
    if response.code != 200:
        return None

    data = json_decode(response.body)

    return data
