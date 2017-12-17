from ._node import Node
from webnode.utils._wsgiutil import content_type


def from_resbot_api(apis, handlers={}, verbose=False):
    """
    Build webnode from resbot api
    :param apis: Json format api docuemnt which conform to the Resbot api specifiction
    :param verbose: Control whether dump the node tree
    :return: webnode
    """

    root_node = Node('')

    for name, api in apis.items():

        parent_node = root_node
        paths = [p for p in api.get('path', '').split('/') if p]

        http_method = api.get('method', 'GET')
        auth = api.get('__auth', False)

        for node in paths:
            child_node = parent_node.get_child(node)
            child_node = child_node if child_node else Node(node, parent_node, auth=auth)
            parent_node = child_node

        # Only the path's last node has a handler
        handler = handlers.get(name, default_handler)
        if handler and child_node:
            child_node.set_handler(http_method, handler)

    if verbose:
        root_node.dump_tree_path()

    return root_node


@content_type("application/json")
def default_handler(**kwargs):
    return "Webnode default response!"
