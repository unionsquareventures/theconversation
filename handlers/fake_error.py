from base import BaseHandler
from lib.auth import admin_only

class FakeErrorHandler(BaseHandler):
    def get(self):
        error = Unknown()
