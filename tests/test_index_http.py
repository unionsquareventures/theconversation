import sys
sys.path.append('../')
from server import init_app
from tornado.testing import AsyncHTTPTestCase
from models import UserInfo

class TestIndexHTTP(AsyncHTTPTestCase):
    def startUp(self):
        u = UserInfo(user=User(**user_info['user']),
                            access_token=AccessToken(**user_info['access_token']))
        u.save()

    def tearDown(self):
        UserInfo.objects().delete()

    def get_app(self):
        return init_app(auth_passthrough=True)

    def test_index_page(self):
        self.http_client.fetch(self.get_url('/'), self.stop, follow_redirects=True)
        response = self.wait()
        self.assertEqual(response.code, 200)

