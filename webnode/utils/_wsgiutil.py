from wsgiref.util import request_uri
from urlparse import urlparse
import httplib
import cherrypy


def webnode_wsgi_app(webnodes, environ, start_response):

    paths = [p for p in urlparse(request_uri(environ)).path.split('/') if p]
    http_method = environ.get("REQUEST_METHOD", "GET")

    webnode_environ = environ

    try:
        response = webnodes.response(paths, http_method, **webnode_environ)
        status = '200 OK'
        headers = [('Content-type', 'text/plain')]
        start_response(status, headers)

        return [response]
    except cherrypy.HTTPError as e:
        status = '{} {}'.format(e.code, httplib.responses[e.code])
        headers = [('Content-type', 'text/plain')]

        return [str(e)]