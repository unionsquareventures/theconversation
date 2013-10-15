import settings
import tornado.web
import tornado.auth
import tornado.httpserver
import json
from raven.contrib.tornado import SentryMixin
from urlparse import urlparse
from models.user_info import UserInfo, User
import os
import httplib

class BaseHandler(SentryMixin, tornado.web.RequestHandler):
    def __init__(self, *args, **kwargs):
        super(BaseHandler, self).__init__(*args, **kwargs)
        username = self.get_current_username()
        base_url = "http://" + settings.base_url
        self.vars = {
                        'path': self.request.path,
                        'base_url': base_url,
                        'username': username,
                        'user_id_str': self.get_current_user_id_str(),
                        'user_email_address': self.get_secure_cookie('email_address') or '',
                        'settings': settings,
                        'is_admin': self.is_admin,
                        'is_staff': self.is_staff,
                        'is_blacklisted': self.is_blacklisted(username),
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
        username = self.get_cookie('usv_username') or False
        return username
        
    def is_staff(self, username):
        if username.lower() in settings.staff_twitter_handles:
            return True
        return False

    def is_blacklisted(self, username):
        u = UserInfo.objects(user__username=username).first()
        if u and u.user.is_blacklisted:
            return True
        return False

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

    def get(self, id='', username='', action=''):
        id_str = self.get_current_user_id_str()
        username = self.get_current_username()
        if id_str and not username:
            self.clear_all_cookies()
            self.redirect('/')

        if action == 'new' and not id:
            self.new()
        elif self.request.path == "/posts/new" or  self.request.path.find('/posts/new?') == 0:
            self.new()
        elif action == 'edit' and id:
            self.edit(id)
        elif action == '' and id:
            self.detail(id)
        else:
            self.index()
    
    def write_error(self, status_code, **kwargs):
        self.require_setting("static_path")
        if status_code in [404, 500, 503, 403]:
            filename = os.path.join(self.settings['static_path'], '%d.html' % status_code)
            if os.path.exists(filename):
                f = open(filename, 'r')
                data = f.read()
                f.close()
                return self.write(data)
        return self.write("<html><title>%(code)d: %(message)s</title>" \
                "<body class='bodyErrorPage'>%(code)d: %(message)s</body></html>" % {
            "code": status_code,
            "message": httplib.responses[status_code],
        })

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

