import httplib
import unittest
from webnode.node import from_resbot_api
from webnode import HTTPError
from webnode import HTTP_UNAUTHORIZED_ERROR


class Test(unittest.TestCase):

    def test_from_resbot_api(self):

        apis = {
            'api1':{
                "method": "POST",
                "path": "/a/b"
            },
            'api_sensitive': {
                "method": "GET",
                "path": "/sensitive",
                "__auth": True
            }
        }

        webnodes = from_resbot_api(apis, verbose=True)

        self.assertEqual('Webnode default response!', webnodes.response(['a','b'], 'post'))

        try:
            webnodes.response(['a', 'b'], 'get')
        except HTTPError as e:
            self.assertEqual(e.status, httplib.METHOD_NOT_ALLOWED)

        try:
            webnodes.response(['non-existent'], 'get')
        except HTTPError as e:
            self.assertEqual(e.status, httplib.NOT_FOUND)

        try:
            webnodes.response(['sensitive'], 'get')
        except HTTP_UNAUTHORIZED_ERROR as e:
            self.assertEqual(e.status, httplib.UNAUTHORIZED)