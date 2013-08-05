import settings
import tornado.web
import tornado.auth
import tornado.httpserver
from models.user_info import UserInfo, User, AccessToken
from base import BaseHandler

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

        if not user_obj['username'].lower() in settings.allowed_users:
            raise tornado.web.HTTPError(401, "Not authorized.")

        user = {
                'auth_type': 'twitter',
                'id_str': user_obj['id_str'],
                'username': user_obj['username'],
                'fullname': user_obj['name'],
                'screen_name': user_obj['screen_name'],
                'profile_image_url': user_obj['profile_image_url'],
                'profile_image_url_https': user_obj['profile_image_url_https'],
        }
        self.set_secure_cookie("user_id_str", user_obj['id_str'])
        access_token = user_obj['access_token']
        u = UserInfo.objects(user__id_str=user['id_str']).first()
        if u:
            u.user = User(**user)
            u.access_token = AccessToken(**access_token)
        else:
            u = UserInfo(user=User(**user), access_token=AccessToken(**access_token))
        u.save()
        self.redirect("/")

class LogoutHandler(BaseHandler):
    @tornado.web.asynchronous
    def get(self):
        self.clear_cookie("user_id_str")
        self.redirect("/")
