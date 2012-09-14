import settings
import tornado.web
import tornado.auth
import tornado.httpserver
import sys
import os
import mimetypes
import json
from minifier import Minifier
import urlparse
import forms

from base import BaseHandler
from post import PostHandler

log = settings.log
minifier = Minifier()

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


# Main page
class IndexHandler(BaseHandler):
    def get(self):
        self.render('templates/index.html', **self.vars)


if __name__ == '__main__':
    log.info('Starting server on port 8888')
    application = tornado.web.Application([
        (r'/', IndexHandler),
        (r'/auth/twitter/', TwitterLoginHandler),
        # Posts
        (r'/posts(?:/(<id>.*))?', PostHandler),
    ], **settings.tornado_config)
    http_server = tornado.httpserver.HTTPServer(application)#, ssl_options={
    #        "certfile": os.path.join("/", "sub.mydomain.com.crt"),
    #        "keyfile": os.path.join("/", "sub.mydomain.com.key")
    #})
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
