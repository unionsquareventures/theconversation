import sys
sys.path.append('../')
from server import init_app
from tornado.testing import AsyncHTTPTestCase

class TestIndexHTTP(AsyncHTTPTestCase):
    def get_app(self):
        return init_app()

    def test_index_page(self):
        self.http_client.fetch(self.get_url('/'), self.stop)
        response = self.wait()
        self.assertEqual(response.code, 401)

