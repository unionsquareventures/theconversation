import settings
import tornado.web
import tornado.auth
import tornado.httpserver

from base import BaseHandler

allowed_usernames = [
    '_zachary',
]

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

        if not user_obj['username'] in allowed_usernames:
            raise tornado.web.HTTPError(401, "Not authorized.")

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
