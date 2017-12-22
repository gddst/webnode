from ._node import Node
from webnode.utils._wsgiutil import content_type


def from_resbot_api(apis, base_path=None, handlers=None, verbose=False):
    """
    Build webnode from resbot api
    :param apis: Json format api docuemnt which conform to the Resbot api specifiction
    :param base_path:
    :param handlers:
    :param verbose: Control whether dump the node tree
    :return: webnode
    """
    root_node = Node('')
    if base_path:
        paths = [p for p in base_path.split('/') if p]
        for path in paths:
            root_node = Node(path, root_node)

    for name, api in apis.items():

        parent_node = root_node
        paths = [p for p in api.get('path', '').split('/') if p]

        http_method = api.get('method', 'GET')
        auth = api.get('__auth', False)

        for node_path in paths:
            child_node = None
            child_node = parent_node.get_child_(node_path)
            child_node = child_node if child_node else Node(node_path, parent_node, auth=auth)
            parent_node = child_node

        # Only the path's last node has a handler
        if handlers is None:
            handlers = {}

        handler = handlers.get(name, default_handler)
        if handler and child_node:
            child_node.set_handler(http_method, handler)

    if verbose:
        root_node.dump_tree_path()

    return root_node


@content_type("application/json")
def default_handler(**kwargs):
    return "Webnode default response!"
