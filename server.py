import settings
import pymongo
import tornado.web
import tornado.auth
import tornado.httpserver
import sys
import os
import mimetypes
import json
from minifier import Minifier
import urlparse

log = settings.log
conn = pymongo.Connection('localhost', 27017, socketTimeoutMS=50)
minifier = Minifier()


class BaseHandler(tornado.web.RequestHandler):
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


class TwitterLoginHandler(BaseHandler, tornado.auth.TwitterMixin):
    @tornado.web.asynchronous
    def get(self):
        if self.get_argument("oauth_token", None):
            self.get_authenticated_user(callback=self.async_callback(self._on_login))
            return
        self.authorize_redirect()

    def _on_login(self, user):
        if not user:
            raise tornado.web.HTTPError(500, "Twitter authentication failed.")
        self.set_secure_cookie("user", tornado.escape.json_encode(user))
        self.redirect("/")


class IndexHandler(BaseHandler):
    @tornado.web.authenticated
    @tornado.web.asynchronous
    def get(self):
        vars = {'username': self.get_current_user()['username']}
        self.render('templates/index.html', **vars)


if __name__ == '__main__':
    log.info('Starting server on port 8888')
    application = tornado.web.Application([
        (r'/auth/twitter/', TwitterLoginHandler),
        (r'/', IndexHandler),
    ], **settings.tornado_config)
    http_server = tornado.httpserver.HTTPServer(application)#, ssl_options={
    #        "certfile": os.path.join("/", "sub.mydomain.com.crt"),
    #        "keyfile": os.path.join("/", "sub.mydomain.com.key")
    #})
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
