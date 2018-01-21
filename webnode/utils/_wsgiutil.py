from wsgiref.util import request_uri
try:
    from urllib.parse import urlencode  # 3
except:
    from urllib import urlencode  # 2
try:
    from http import client as httpclient  # 3
except:
    import httplib as httpclient  # 2
from urllib.parse import urlparse
import functools
from webnode import HTTPError


def webnode_wsgi_app(webnodes, environ, start_response):

    paths = [p for p in urlparse(request_uri(environ)).path.split('/') if p]
    http_method = environ.get("REQUEST_METHOD", "GET")

    webnode_environ = environ

    try:
        response, response_type, status = webnodes.response(paths, http_method, **webnode_environ)
        headers = [('Content-type', response_type)]
        start_response(status, headers)
        response = bytes(response, encoding="utf-8")
        return [response]
    except HTTPError as e:
        status = '{} {}'.format(e.status, httpclient.responses[e.status])
        headers = [('Content-type', 'text/plain')]
        start_response(status, headers)
        return [bytes(str(e), encoding="utf-8")]


def content_type(response_type):
    def handler(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs), response_type
        return wrapper
    return handler


def load_webnode_handler(conf):
    handlers = {}

    for name, loader in list(conf.items()):
        handlers[name] = loader

    return handlers

