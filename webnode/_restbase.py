'''
Created on Oct 19, 2015

@author: gddst
'''
import httplib
import json
import logging
import traceback

import cherrypy

from resbot.common.constants import ContentType
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
        cherrypy.response.headers[http_header.CONTENT_TYPE] = ContentType.ApplicationJson

        httpmethod = cherrypy.request.method
        
        try:
            request_user = cherrypy.session.get('user')
            if request_user is not None:
                params['req_user_info']=request_user 
                return self._root_node.response(vpath, httpmethod, **params)
            else:
                raise cherrypy.HTTPError(401)
            
        except cherrypy.HTTPRedirect:
            raise
        except cherrypy.HTTPError, e:
            err_logger.debug(traceback.format_exc())
            return http_error_handler(e.status)
        except HTTPError, e:
            err_logger.debug(traceback.format_exc())
            return http_error_handler(e.status)
        except Exception ,e :
            err_logger.debug(traceback.format_exc())
            traceback.print_exc()
            return http_error_handler(500)
            
def http_error_handler(status):
    cherrypy.serving.response.status = status
    cherrypy.response.headers[http_header.CONTENT_TYPE] = ContentType.TextHtml
    return Renderer.render('error/plain', status=status,
                           reason=httplib.responses.get(status))