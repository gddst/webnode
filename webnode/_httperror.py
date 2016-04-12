'''
Created on Dec 16, 2015

@author: gddst
'''
import httplib


class HTTPError(Exception):
    '''
    classdocs
    '''
    
    def __init__(self, status):
        self.status = status
        
    def __str__(self):
        return repr(self.status)
    
    
class HTTP_UNAUTHORIZED_ERROR(HTTPError):
    
        def __init__(self, status=httplib.UNAUTHORIZED):
            super(HTTP_UNAUTHORIZED_ERROR, self).__init__(status)