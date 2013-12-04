from base import BaseHandler

class FakeErrorHandler(BaseHandler):
    def get(self):
        raise Exception("Testing...")
