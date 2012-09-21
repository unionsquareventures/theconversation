import settings
import tornado.web
import tornado.auth
import tornado.httpserver

import pymongo

conn = pymongo.Connection('localhost', 27017, socketTimeoutMS=50)

class BaseHandler(tornado.web.RequestHandler):
    def __init__(self, *args, **kwargs):
        super(BaseHandler, self).__init__(*args, **kwargs)
        self.vars = {
                        'user': self.get_current_user(),
                    }

    @property
    def db(self):
        if not hasattr(self, '_db'):
            self._db = conn['usv']
        return self._db

    def render_json(self, obj):
        resp = json.dumps(obj)
        callback = self.get_argument("callback", None)
        if callback:
            resp = "%s(%s)" % (callback, resp)
        self.write(resp)
        self.finish()

    def get_current_user(self):
        user_json = self.get_secure_cookie("user")
        if not user_json: return None
        return tornado.escape.json_decode(user_json)
