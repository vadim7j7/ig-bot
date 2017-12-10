from tornado.escape import json_decode

from bot.src.urls import URL_FEED
from bot.src.client import Client


async def full_feed() -> dict:
    response = await Client.send_request(URL_FEED)
    return json_decode(response.body)
