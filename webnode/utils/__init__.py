from functools import partial
from ._wsgiutil import webnode_wsgi_app
from ._wsgiutil import content_type

def to_wsgi_app(webnodes):
    return partial(webnode_wsgi_app, webnodes)