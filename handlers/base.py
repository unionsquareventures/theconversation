import settings
import tornado.web
import tornado.auth
import tornado.httpserver
import json
from raven.contrib.tornado import SentryMixin

class BaseHandler(SentryMixin, tornado.web.RequestHandler):
    def __init__(self, *args, **kwargs):
        super(BaseHandler, self).__init__(*args, **kwargs)
        self.vars = {
                        'user': self.get_current_user(),
                        'settings': settings,
                        'is_admin': self.is_admin,
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
        if not user_json: return {}
        return tornado.escape.json_decode(user_json)

    def is_admin(self):
        user = self.get_current_user()
        if user and user['id_str'] in settings.admin_user_ids:
            return True
        return False

    @tornado.web.authenticated
    def post(self, id='', action=''):
        if id:
            self.update(id)
        else:
            self.create()

    @tornado.web.authenticated
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

