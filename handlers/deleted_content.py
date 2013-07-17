from base import BaseHandler
from models import Post
import tornado.web

class DeletedContentHandler(BaseHandler):
    def get(self):
        if not self.is_admin():
            raise tornado.web.HTTPError(403)

        cur_page = 0
        length = 50
        deleted_content = Post.objects(deleted=True).order_by('-date_created')[cur_page*length:cur_page+length]
        self.vars.update({
            'deleted_content': deleted_content,
        })
        self.render('deleted_content/index.html', **self.vars)
