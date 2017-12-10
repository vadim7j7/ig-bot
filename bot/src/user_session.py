import time
from tornado.escape import json_decode

from bot.src.structures import Credentials
from bot.src.urls import URL_HOME, URL_SIGN_IN, URL_PRIVATE_PAGE
from bot.src.utils import list_to_cookies
from bot.src.client import Client
from bot.src.storage import get_data


class UserSession(object):
    def __init__(self, credentials: Credentials):
        self.credentials = credentials

    def init_session(self):
        Client.session_id = self.credentials.email

        session = get_data(Client.session_id)
        if session is not None:
            Client.cookies = list_to_cookies(session)

    async def login(self) -> bool:
        """
        >> user_session = UserSession(user.credentials)
        >> user_session.init_session()
        >> result = await user_session.login()
        True or False
        """

        if Client.cookies is None:
            if not await self.sign_in():
                return False
        else:
            if not await self.check_login():
                result = await self.sign_in()
                return result

        return True

    async def sign_in(self) -> bool:
        """
        >> user_session = UserSession(user.credentials)
        >> result = await user_session.sign_in()
        True or False
        """
        response = await Client.send_request(url=URL_HOME)
        if response.code != 200:
            return False

        time.sleep(3)

        body = {'username': self.credentials.email, 'password': self.credentials.password}
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        response = await Client.send_request(url=URL_SIGN_IN, method='POST', body=body, headers=headers)

        if response.code != 200:
            if response.code == 400:
                # Send email to confirm account
                url = json_decode(response.body).get('checkpoint_url', None)
                result = await self.check_account(url)
                return result

        return True

    async def check_account(self, url: str) -> bool:
        url = '{}{}'.format(URL_HOME, url)
        body = {'choice': 1}

        response = await Client.send_request(url=url, method='POST', body=body)
        if response.code is not 200:
            return False

        # TODO it needs to change for UI
        # Waiting get code
        code = ''
        while len(code) < 6:
            code = input('Please enter code for %s:' % self.credentials.email)

        # Send code
        body = {'security_code': code}
        response = await Client.send_request(url=url, method='POST', body=body)

        return response.code == 200

    @staticmethod
    async def check_login() -> bool:
        response = await Client.send_request(URL_PRIVATE_PAGE)

        return response.code == 200
