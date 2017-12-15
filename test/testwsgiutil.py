from webnode.utils import to_wsgi_app
from webnode.node import Node
from wsgiref.simple_server import make_server
from werkzeug.serving import run_simple

def testwsgiutil():
    root = Node('')
    webnodes = Node("root", root, auth=False)
    root.dump_tree_path()

    webnodes.get(lambda **kwargs: "hello world")

    app = to_wsgi_app(root)
    run_simple('127.0.0.1', 5000, app, use_debugger=True, use_reloader=False)

if __name__=='__main__':
    testwsgiutil()