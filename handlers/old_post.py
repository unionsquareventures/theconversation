from base import BaseHandler
import tornado

class OldPostHandler(BaseHandler):
    def get(self, year, month, slug):
        url = '/%s/%s/%s.php' % (year, month, slug)
        new_url = self.settings['old_post_urls'].get(url)
        if not new_url:
            raise tornado.web.HTTPError(404)
        else:
            self.redirect(new_url)
