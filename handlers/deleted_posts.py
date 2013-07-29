from base import BaseHandler
from models import Post
import tornado.web

class DeletedPostsHandler(BaseHandler):
    def get(self):
        if not self.is_admin():
            raise tornado.web.HTTPError(403)

        cur_page = 0
        per_page = 20
        deleted_posts = Post.objects(deleted=True).order_by('-date_created')[cur_page*length:cur_page+length]
        self.vars.update({
            'deleted_posts': deleted_posts,
        })
        self.render('deleted_posts/index.html', **self.vars)
