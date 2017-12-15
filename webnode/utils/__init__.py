from functools import partial
from ._wsgiutil import webnode_wsgi_app

def to_wsgi_app(webnodes):
    return partial(webnode_wsgi_app, webnodes)