import sys
sys.path.append('../')
from server import init_app
from tornado.testing import AsyncHTTPTestCase

class TestPostHTTP(AsyncHTTPTestCase):
    def get_app(self):
        return init_app(bundle=False)

    # Hackpad endpoint
    def test_hackpad_endpoint(self):
        self.http_client.fetch(self.get_url('/generate_hackpad'), self.stop)
        response = self.wait()
        self.assertEqual(response.code, 401)

