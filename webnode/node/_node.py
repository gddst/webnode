'''
Created on Dec 16, 2015

@author: gddst
'''

import httplib
import re

from webnode import HTTPError
from webnode._httperror import HTTP_UNAUTHORIZED_ERROR
from webnode.renderer import Renderer


class Node( object ):
    
    def __init__(self, path_name, parent=None, auth=True ):
        
        self.__path_name = path_name
        self.__parent = parent
        self.__children = {}
        self.__handler = {}
        self._auth=auth
        
        if parent:
            parent.add_child( self )
        
    def add_child(self,child):
        
        if not self.__children.has_key( child.__path_name ):
            self.__children[ child.__path_name ]=child
            
    def update_child(self,child):
        if self.__children.has_key( child.__path_name ):
            self.__children[ child.__path_name ]=child        
            
    def get_child(self,child_path_name):
        
        if self.__children.has_key( child_path_name ):
            return self.__children[child_path_name]
        else:
            for key in self.__children.keys():
                if Node.__path_match(child_path_name, key):
                    return self.__children[key]
        return None
    
    def remove_child(self,child):
        if self.__children.has_key( child.__path_name ):
            self.__children.pop( child.__path_name )
    
    def get_full_path(self):
                
        if not self.__parent:
            return self.__path_name
        else:
            return "{}/{}".format( self.__parent.get_full_path(), self.__path_name )
        
    def dump_tree_path(self):
        print self.get_full_path()
        if self.__children:
            for child in self.__children:
                self.__children[child].dump_tree_path()

    def get_path_name(self):
        return self.__path_name
    
    def get_handlers(self):
        return self.__handler

    def response(self,sub_path, http_method,**params):
        
        if not sub_path:
            if self._auth and params.get('req_user_info') is None:
                raise HTTP_UNAUTHORIZED_ERROR()
            
            if self.__handler.has_key(http_method):
                return self.__handler[http_method](**params)
            else:
                raise HTTPError( httplib.METHOD_NOT_ALLOWED )
        else:
            child = self.get_child(sub_path[0])            
            if child:
                param_name = self.__parse_para(child.get_path_name())
                if param_name:
                    param_name=param_name[0]
                    param_value=self.__path_match(sub_path[0], child.get_path_name())
                    if param_value:
                        params[param_name]=param_value
                return child.response( sub_path[1:], http_method, **params )
            else:
                raise HTTPError( httplib.NOT_FOUND )
    
    def get(self, handler):
        self.__handler['GET']=handler
        
    def post(self, handler):
        self.__handler['POST']=handler
        
    def put(self, handler):
        self.__handler['PUT']=handler
            
    def delete(self, handler):
        self.__handler['DELETE']=handler
            
    def head(self, handler):
        self.__handler['HEAD']=handler
            
    def options(self, handler):
        self.__handler['OPTIONS']=handler

    @staticmethod
    def __parse_para( sub_path):
        return re.findall(r"{(.+?)}", sub_path )
    
    @staticmethod
    def __path_match( sub_path, node_path):
        
        if re.match(r".*{.*}.*", node_path):
            prefix = re.findall(r"(.+?){", node_path )
            if prefix:
                prefix=prefix[0]
                if not sub_path.startswith( prefix ):
                    return False
            else:
                prefix=''
                            
            postfix = re.findall(r"}(.+?)", node_path )
            if postfix:
                postfix=postfix[0]
                if not sub_path.endswith( postfix ):
                    return False
            else:
                postfix=''
            return sub_path[len(prefix):len(sub_path)-len(postfix)]
        else:
            return False
            
    
class ViewNode( Node ):
    
    def __init__(self, path_name, parent , template_name, **kwargs ):
        
        super( ViewNode, self ).__init__(path_name, parent, auth=kwargs.get('auth',True))
        self.template_name = template_name
        self.kwargs=kwargs
        
    def response(self,sub_path, http_method, **params):
        
        if not sub_path and http_method=='GET':
            if self._auth and params.get('req_user_info') is None:
                raise HTTP_UNAUTHORIZED_ERROR()
            return Renderer.render(self.template_name, **dict(self.kwargs,**params))
        else:
            return super( ViewNode, self ).response(sub_path, http_method, **params)
        
                
if __name__=='__main__':
    prefix = 'a'
    postfix = 'b'
    print 'asdb'[len(prefix):len('asdb')-len(postfix)]
    """
    #Testing code
    
    def handler( **params ):
        print '{} response'.format( params['name'] )
    
    root = Node('root')
    index = ViewNode( 'index',root,'hello_world' )
    
    sub_node1 = Node('sub_node1',root)
    sub_node1.register_handler(handler, 'GET')
    def a():
        print 'customized handler'
    leaf_1_a =  Node('leaf_1_a',sub_node1)
    leaf_1_a.register_handler(handler, 'POST')
    leaf_1_a.register_handler(a)
    leaf_1_b =  Node('leaf_1_b',sub_node1)
    
    sub_node2 = Node('sub_node2',root)
    leaf_2_a =  Node('leaf_2_a',sub_node2)
    leaf_2_b =  Node('leaf_2_b',sub_node2)
    sub_node3 = Node('sub_node3',root)
    #print c.get_full_path()
    #root.dump_tree_path()
    root.response(['sub_node1'],'GET',name='sub_node1')
    root.response(['sub_node1','leaf_1_a'],'POST',name='leaf_1_a')
    root.response(['index'],None)
    """

    