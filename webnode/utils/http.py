

class HttpMethod(object):
    
    def __init__(self):
        pass
    
    @property
    def GET(self):
        return 'GET'
    
    @property
    def POST(self):
        return 'POST'
    
    @property
    def PUT(self):
        return 'PUT'
    
    @property
    def DELETE(self):
        return 'DELETE'
    
    @property
    def HEAD(self):
        return 'HEAD'
    
    @property
    def OPTIONS(self):
        return 'OPTIONS'        
    
http_method= HttpMethod()


class HttpHeader(object):
    
    def __init__(self):
        pass

    @property 
    def ACCEPT_LANGUAGE(self):
        return 'Accept-Language'
    @property
    def ACCEPT_RANGES(self):
        return 'Accept-Ranges'
    @property
    def AGE(self):
        return 'Age'
    @property
    def ALLOW(self):
        return 'Allow'
    @property
    def AUTHORIZATION(self):
        return 'Authorization'
    @property
    def CACHE_CONTROL(self):
        return 'Cache-Control'
    @property
    def CONNECTION(self):
        return 'Connection'
    @property
    def CONTENT_ENCODING(self):
        return 'Content-Encoding'
    @property
    def CONTENT_LANGUAGE(self):
        return 'Content-Language'
    @property
    def CONTENT_LENGTH(self):
        return 'Content-Length'
    @property
    def CONTENT_LOCATION(self):
        return 'Content-Location'
    @property
    def CONTENT_MD5(self):
        return 'Content-MD5'
    @property
    def CONTENT_RANGE(self):
        return 'Content-Range'
    @property
    def CONTENT_TYPE(self):
        return 'Content-Type'
    @property
    def DATE(self):
        return 'Date'
    @property
    def ETAG(self):
        return 'ETag'
    @property
    def EXPECT(self):
        return 'Expect'
    @property
    def EXPIRES(self):
        return 'Expires'
    @property
    def FROM(self):
        return 'From'
    @property
    def HOST(self):
        return 'Host'
    @property
    def IF_MATCH(self):
        return 'If-Match'
    @property
    def IF_MODIFIED_SINCE(self):
        return 'If-Modified-Since'
    @property
    def IF_NONE_MATCH(self):
        return 'If-None-Match'
    @property
    def IF_RANGE(self):
        return 'If-Range'
    @property
    def IF_UNMODIFIED_SINCE(self):
        return 'If-Unmodified-Since'
    @property
    def LAST_MODIFIED(self):
        return 'Last-Modified'
    @property
    def LOCATION(self):
        return 'Location'
    @property
    def MAX_FORWARDS(self):
        return 'Max-Forwards'
    @property
    def PRAGMA(self):
        return 'Pragma'
    @property
    def PROXY_AUTHENTICATE(self):
        return 'Proxy-Authenticate'
    @property
    def PROXY_AUTHORIZATION(self):
        return 'Proxy-Authorization'
    @property
    def RANGE(self):
        return 'Range'
    @property
    def REFERER(self):
        return 'Referer'
    @property
    def RETRY_AFTER(self):
        return 'Retry-After'
    @property
    def SERVER(self):
        return 'Server'
    @property
    def TE(self):
        return 'TE'
    @property
    def TRAILER(self):
        return 'Trailer'
    @property
    def TRANSFER_ENCODING(self):
        return 'Transfer-Encoding'
    @property
    def UPGRADE(self):
        return 'Upgrade'
    @property
    def USER_AGENT(self):
        return 'User-Agent'
    @property
    def VARY(self):
        return 'Vary'
    @property
    def VIA(self):
        return 'Via'
    @property
    def WARNING(self):
        return 'Warning'
    @property
    def WWW_AUTHENTICATE(self):
        return 'WWW-Authenticate'
    
http_header= HttpHeader()

__all__ = [
    http_method,
    http_header
]