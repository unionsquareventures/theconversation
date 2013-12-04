import sys
sys.path.append('../')
from server import init_app
from tornado.testing import AsyncHTTPTestCase
from urlparse import urlparse

class TestPostHTTP(AsyncHTTPTestCase):
    def get_app(self):
        return init_app(bundle=False, auth_passthrough=True)

    # Hackpad endpoint
    def test_hackpad_endpoint(self):
        self.http_client.fetch(self.get_url('/generate_hackpad'), self.stop)
        response = self.wait()
        self.assertEqual(response.code, 200)
        print response.body
        url = urlparse(response.body)
        print url.netloc
        self.assertTrue(url.netloc.endswith('hackpad.com'))
        self.assertTrue(len(url.path) > 4)

