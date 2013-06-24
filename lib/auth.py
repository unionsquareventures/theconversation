import settings
import tornado.web

def admin_only(f):
    def wrap(f_self, *args, **kwargs):
        cur_user = f_self.get_current_user()
        if cur_user and cur_user.get('username') in settings.admin_users:
            f(f_self, *args, **kwargs)
        else:
            raise tornado.web.HTTPError(403)
    return wrap
