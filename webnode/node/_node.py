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

        self.__router=None

        if parent:
            parent.add_child( self )

    def response(self,sub_path, http_method,**kwargs):
        # TODO Authentication
        # TODO Parameter extraction
        if self.__router is None:
            self.__router={}
            self.build_router(self.__router)
        print self.__router

        handlers = self.__match_route(sub_path)
        if handlers:
            print "@@@@@ Routing Success", handlers
            handler = handlers.get(http_method.upper())
            if handler:
                return handler(**kwargs)
            else:
                raise HTTPError(httplib.METHOD_NOT_ALLOWED)
        else:
            raise HTTPError(httplib.NOT_FOUND)

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

    def get_handle_children(self,child_path_name):
        children = []
        if child_path_name in self.__children:
            children.append(self.__children[child_path_name])
        else:
            for key in self.__children:
                if Node.__path_match(child_path_name, key):
                    child = self.__children[key]
                    children.append(child)
        return children

    def remove_child(self,child):
        if self.__children.has_key( child.__path_name ):
            self.__children.pop( child.__path_name )

    def get_full_path(self):

        if not self.__parent:
            return self.__path_name
        else:
            return "{}/{}".format( self.__parent.get_full_path(), self.__path_name )

    def dump_tree_path(self):
        if self.__handler.keys():
            print self.get_full_path()
            print self.__handler.keys()
        if self.__children:
            for child in self.__children:
                self.__children[child].dump_tree_path()

    def build_router(self, router):

        path = self.get_full_path()
        for method, handler in self.__handler.iteritems():
            router.setdefault(path,{})
            router[path][method] = handler

        if self.__children:
            for child in self.__children:
                self.__children[child].build_router(router)

    def get_path_name(self):
        return self.__path_name

    def get_handlers(self):
        return self.__handler

    def response_(self,sub_path, http_method,**params):

        http_method = http_method.upper()

        if not sub_path:
            if self._auth and params.get('req_user_info') is None:
                raise HTTP_UNAUTHORIZED_ERROR()

            if self.__handler.has_key(http_method):
                return self.__handler[http_method](**params)
            else:
                raise HTTPError( httplib.METHOD_NOT_ALLOWED )
        else:
            if len(sub_path)==1:
                child = self.get_child(sub_path[0], method=http_method)
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

    def set_handler(self, method, handler):
        self.__handler[method.upper()] = handler

    def options(self, handler):
        self.__handler['OPTIONS']=handler

    def __match_route(self, request_paths):
        request_path_size = len(request_paths)
        for route, handlers in self.__router.iteritems():
            route_paths = [p for p in route.split('/') if p]
            print route_paths
            print handlers
            print request_paths

            if request_path_size!=len(route_paths):
                continue

            match_tuples = zip(route_paths, request_paths)

            for y in match_tuples:
                route_p = y[0]
                request_p = y[1]
                # TODO
                if route_p==request_p:
                    continue

                if Node.__path_match( request_p, route_p):
                    continue
                else:
                    break
            else:
                return handlers

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
