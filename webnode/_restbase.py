'''
Created on Oct 19, 2015

@author: gddst
'''
try:
    from http import client as httpclient  # 3
except:
    import httplib as httpclient  # 2
import logging
import traceback

import cherrypy

from webnode._httperror import HTTPError
from webnode.renderer import Renderer
from webnode.utils.http import http_header


class RESTBase(object):
    
    def __init__(self):
        pass
    
    @cherrypy.expose
    def default(self, *vpath, **params):
        
        err_logger=logging.getLogger('error')
        
        # Set the default content type to application/json
        cherrypy.response.headers[http_header.CONTENT_TYPE] = "application/json;charset=utf-8"

        httpmethod = cherrypy.request.method
        
        try:
            request_user = cherrypy.session.get('user')
            if request_user is not None:
                params['req_user_info']=request_user
                request_paths =  [p for p in self._root_node.get_full_path().split('/') if p]
                request_paths.extend(vpath)
                return self._root_node.response(request_paths, httpmethod, **params)
            else:
                raise cherrypy.HTTPError(401)
            
        except cherrypy.HTTPRedirect:
            raise
        except cherrypy.HTTPError as e:
            err_logger.debug(traceback.format_exc())
            return http_error_handler(e.status)
        except HTTPError as e:
            err_logger.debug(traceback.format_exc())
            return http_error_handler(e.status)
        except Exception as e :
            err_logger.debug(traceback.format_exc())
            traceback.print_exc()
            return http_error_handler(500)


def http_error_handler(status):
    cherrypy.serving.response.status = status
    cherrypy.response.headers[http_header.CONTENT_TYPE] = "text/html;charset=utf-8"
    return Renderer.render('error/plain', status=status,
                           reason=httpclient.responses.get(status))

