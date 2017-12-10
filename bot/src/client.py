from urllib.parse import urlencode
from tornado.httpclient import AsyncHTTPClient, HTTPRequest, HTTPResponse

from bot.src.urls import HOST, URL_HOME
from bot.src.utils import headers_to_cookies, cookies_to_list
from bot.src.storage import save_data


user_agent = ("Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/48.0.2564.103 Safari/537.36")
accept_language = 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4'


def http_request(url: str, method: str, body: str = None, addition_headers: dict = None) -> HTTPRequest:
    """
    Generate http request
    >> request = http_request(url: 'https://google.com')
    """

    headers = {
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': accept_language,
        'Connection': 'keep-alive',
        'Content-Length': '0',
        'Host': HOST,
        'Origin': URL_HOME,
        'Referer': '%s/' % URL_HOME,
        'User-Agent': user_agent,
        'X-Instagram-AJAX': '1',
        'X-Requested-With': 'XMLHttpRequest'
    }

    if addition_headers is not None:
        headers.update(addition_headers)

    return HTTPRequest(url=url, method=method, headers=headers, body=body, follow_redirects=True, validate_cert=False)


def http_client():
    """
    >> response = http_client.fetch(request: http_request(...))
    :return: AsyncHTTPClient
    """
    return AsyncHTTPClient()


class Client(object):
    session_id = None
    cookies = None

    @staticmethod
    def raw_cookie():
        if Client.cookies:
            return cookies_to_list(cookies=Client.cookies)

    @staticmethod
    async def send_request(url: str, method: str = 'GET', body: dict = None, headers: dict = None) -> HTTPResponse:
        """
        >> response = send_request(url: 'https://www.google.ru', body: {'q': 'hello'})
        """

        # Conver dict to str body
        if body is not None:
            body = urlencode(body)

        # Add cookies to header
        if Client.cookies is not None:
            if headers is None:
                headers = {}

            headers['Cookie'] = '; '.join('%s=%s' % (key, Client.cookies[key].value) for key in Client.cookies)

            if not method == 'GET' and Client.cookies['csrftoken'] and Client.cookies['csrftoken'].value:
                headers['X-CSRFToken'] = Client.cookies['csrftoken'].value

        # Generate http request and send to a server
        request = http_request(url=url, method=method, body=body, addition_headers=headers)
        response = await http_client().fetch(request=request, raise_error=False)

        # Save some cookies in memory and in storage
        headers = response.headers
        Client.cookies = headers_to_cookies(headers)
        save_data(Client.session_id, Client.raw_cookie())

        return response
