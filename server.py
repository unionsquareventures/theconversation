import settings
import tornado.web
import tornado.auth
import tornado.httpserver
import sys
import os
import mimetypes
import json
import urlparse
import forms

from handlers import BaseHandler, PostHandler, DisqusHandler

log = settings.log

class TwitterLoginHandler(BaseHandler, tornado.auth.TwitterMixin):
    @tornado.web.asynchronous
    def get(self):
        if self.get_argument("oauth_token", None):
            self.get_authenticated_user(callback=self.async_callback(self._on_login))
            return
        self.authorize_redirect()

    def _on_login(self, user_obj):
        if not user_obj:
            raise tornado.web.HTTPError(500, "Twitter authentication failed.")
        user = {
                'auth_type': 'twitter',
                'username': user_obj['username'],
                'screen_name': user_obj['screen_name'],
                'profile_image_url': user_obj['profile_image_url'],
                'profile_image_url_https': user_obj['profile_image_url_https'],
        }
        self.set_secure_cookie("user", tornado.escape.json_encode(user))
        self.set_secure_cookie("user_token", tornado.escape.json_encode({'twitter': user_obj['access_token']}))
        self.redirect("/")


# Main page
class IndexHandler(BaseHandler):
    def get(self):
        self.redirect('/posts')

if __name__ == '__main__':
    log.info('Starting server on port 8888')
    application = tornado.web.Application([
        (r'/', IndexHandler),
        (r'/auth/twitter/', TwitterLoginHandler),
        # Posts
        (r'/posts', PostHandler),
        (r'/posts/(?P<params>.*)$', PostHandler),
        # Disqus
        (r'/disqus', DisqusHandler),
    ], **settings.tornado_config)
    http_server = tornado.httpserver.HTTPServer(application)#, ssl_options={
    #        "certfile": os.path.join("/", "sub.mydomain.com.crt"),
    #        "keyfile": os.path.join("/", "sub.mydomain.com.key")
    #})
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
