from wsgiref.util import request_uri
from urlparse import urlparse
import httplib
import functools
from webnode import HTTPError


def webnode_wsgi_app(webnodes, environ, start_response):

    paths = [p for p in urlparse(request_uri(environ)).path.split('/') if p]
    http_method = environ.get("REQUEST_METHOD", "GET")

    webnode_environ = environ

    try:
        response, response_type = webnodes.response(paths, http_method, **webnode_environ)
        status = '200 OK'
        headers = [('Content-type', response_type)]
        start_response(status, headers)

        return [response]
    except HTTPError as e:
        status = '{} {}'.format(e.status, httplib.responses[e.status])
        headers = [('Content-type', 'text/plain')]
        start_response(status, headers)
        return [str(e)]


def content_type(response_type):
    def handler(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs), response_type
        return wrapper
    return handler


def load_webnode_handler(conf):
    handlers = {}

    for name, loader in conf.items():
        handlers[name] = loader

    return handlers

