from base import BaseHandler

class FakeErrorHandler(BaseHandler):
    def get(self):
        error = Unknown()
