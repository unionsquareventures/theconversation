import sys
sys.path.append('../')
from server import init_app
from tornado.testing import AsyncHTTPTestCase

class TestPostHTTP(AsyncHTTPTestCase):
    def get_app(self):
        return init_app()

    # Post creation as an admin

    # Post creation as a normal user

    # Post by slug

    # Test permissions for admin/non-admin pages

    # Post featuring

    # Search page

    # Featured page

    # Delete a user

    # Upvoting
