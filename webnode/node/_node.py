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
    
    def __init__(self, path_name, parent=None, auth=True , response_type='text/plain'):
        
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

    def get_child_(self, child_path_name):
        """
        Static structure method for node tree creation
        :param child_path_name:
        :return:
        """
        return self.__children.get(child_path_name)

    def get_child(self,child_path_name, method=None):

        if child_path_name in self.__children:
            return self.__children[child_path_name]
        else:
            for key in self.__children:
                if Node.__path_match(child_path_name, key):
                    child = self.__children[key]
                    if method and not method in child.__handler:
                        continue
                    return child
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

        http_method = http_method.upper()

        if not sub_path:
            if self._auth and params.get('req_user_info') is None:
                raise HTTP_UNAUTHORIZED_ERROR()

            if self.__handler.has_key(http_method):
                return self.__handler[http_method](**params)
            else:
                raise HTTPError( httplib.METHOD_NOT_ALLOWED )
        else:
            child = self.get_child(sub_path[0], method=http_method)
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

    def set_handler(self, method, handler):
        self.__handler[method.upper()] = handler

    def options(self, handler):
        self.__handler['OPTIONS']=handler

    def __get_handle_node(self, sub_path, method=None):
        """

        :param sub_path:
        :return:
        """
        if not sub_path:
            return self
        else:
            child = self.get_child(sub_path[0], method=method)
            if child:
                return child.__get_handle_node(sub_path[1:], method=method)

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
