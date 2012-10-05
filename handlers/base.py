import settings
import tornado.web
import tornado.auth
import tornado.httpserver
import json

class BaseHandler(tornado.web.RequestHandler):
    def __init__(self, *args, **kwargs):
        super(BaseHandler, self).__init__(*args, **kwargs)
        self.vars = {
                        'user': self.get_current_user(),
                    }

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

    def post(self, id='', action=''):
        if id:
            self.update(id)
        else:
            self.create()

    def get(self, id='', action=''):
        if action == 'new' and not id:
            self.new()
        elif action == 'edit' and id:
            self.edit(id)
        elif action == '' and id:
            self.detail(id)
        else:
            self.index()

    def new(self):
        raise tornado.web.HTTPError(404)

    def edit(self, id):
        raise tornado.web.HTTPError(404)

    def detail(self, id):
        raise tornado.web.HTTPError(404)

    def index(self):
        raise tornado.web.HTTPError(404)

    def create(self):
        raise tornado.web.HTTPError(404)

    def update(self, id):
        raise tornado.web.HTTPError(404)

