from base import BaseHandler
from models import Post
import tornado.web

class DeletedPostsHandler(BaseHandler):
    def get(self):
        if not self.current_user_can('delete_posts'):
            raise tornado.web.HTTPError(401)
        page = abs(int(self.get_argument('page', '1')))
        per_page = abs(int(self.get_argument('per_page', '10')))
        deleted_posts = Post.objects(deleted=True).order_by('-date_deleted')
        deleted_posts = deleted_posts[(page-1)*per_page:(page-1)*per_page+per_page]
        total_count = Post.objects(deleted=True)\
                                        .order_by('-date_deleted').count()
        self.vars.update({
            'deleted_posts': deleted_posts,
            'total_count': total_count,
            'page': page,
            'per_page': per_page,
        })
        self.render('deleted_posts/index.html', **self.vars)
