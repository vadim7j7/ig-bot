from http.cookies import SimpleCookie
from tornado.httputil import HTTPHeaders


def headers_to_cookies(headers: HTTPHeaders) -> SimpleCookie:
    items = headers.get_list("Set-Cookie")

    return list_to_cookies(items)


def list_to_cookies(items: list) -> SimpleCookie:
    cookies = SimpleCookie()

    for item in items:
        cookies.load(item)

    return cookies


def cookies_to_list(cookies: SimpleCookie) -> list:
    items = list(cookies.items())

    return [morsel.OutputString() for _, morsel in items]
