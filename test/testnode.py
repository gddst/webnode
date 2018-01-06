from webnode.node import Node
from webnode.node import ViewNode


def testnode():

    def handler( **params ):
        print '{} response'.format( params['name'] )

    root = Node('')
    #index = ViewNode( 'index',root,'hello_world' )

    sub_node1 = Node('sub_node1',root)
    sub_node1.set_handler('GET', handler)
    def a():
        print 'customized handler'
    leaf_1_a =  Node('leaf_1_a',sub_node1)
    leaf_1_a.set_handler('POST', handler)
    leaf_1_a.get(a)
    leaf_1_b =  Node('leaf_1_b',sub_node1)

    sub_node2 = Node('sub_node2',root)
    leaf_2_a =  Node('leaf_2_a',sub_node2)
    leaf_2_b =  Node('leaf_2_b',sub_node2)
    sub_node3 = Node('sub_node3',root)

    root.dump_tree_path()
    root.response(['sub_node1'],'GET',name='sub_node1')
    root.response(['sub_node1','leaf_1_a'],'POST',name='leaf_1_a')
    #root.response(['index'],None)
