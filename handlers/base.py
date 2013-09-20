import settings
import tornado.web
import tornado.auth
import tornado.httpserver
import json
from raven.contrib.tornado import SentryMixin
from urlparse import urlparse

class BaseHandler(SentryMixin, tornado.web.RequestHandler):
    def __init__(self, *args, **kwargs):
        super(BaseHandler, self).__init__(*args, **kwargs)
        username = self.get_current_username()
        self.vars = {
                        'username': username,
                        'user_id_str': self.get_current_user_id_str(),
                        'user_email_address': self.get_secure_cookie('email_address') or '',
                        'settings': settings,
                        'is_admin': self.is_admin,
                        'urlparse': urlparse,
                    }
        user_id_str = self.get_current_user_id_str()
        if user_id_str in settings.banned_user_ids:
            raise tornado.web.HTTPError(401)

    def write_json(self, obj):
        resp = json.dumps(obj)
        callback = self.get_argument("callback", None)
        if callback:
            resp = "%s(%s)" % (callback, resp)
        self.write(resp)
        self.finish()

    def get_current_user(self):
        if self.settings.get('auth_passthrough'):
            return settings.test_user_info['user']['id_str']
        return self.get_secure_cookie('user_id_str')

    def get_current_user_id_str(self):
        if self.settings.get('auth_passthrough'):
            return settings.test_user_info['user']['id_str']
        user_id_str = self.get_secure_cookie('user_id_str') or ''
        return user_id_str
    
    def get_current_username(self):
        #if self.settings.get('auth_passthrough'):
        #    return settings.test_user_info['user']['username']
        username = self.get_secure_cookie('username') or 'you'
        return username

    def is_admin(self):
        user_id_str = self.get_current_user_id_str()
        if user_id_str in settings.admin_user_ids:
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

