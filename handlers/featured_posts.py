from base import BaseHandler
from models import Post
import tornado.web

class FeaturedPostsHandler(BaseHandler):
    def get(self):
        page = abs(int(self.get_argument('page', '1')))
        per_page = abs(int(self.get_argument('per_page', '10')))
        featured_posts = Post.objects(deleted=False, featured=True).order_by('-date_featured')
        featured_posts = featured_posts[(page-1)*per_page:(page-1)*per_page+per_page]
        total_count = Post.objects(deleted=False, featured=True)\
                                        .order_by('-date_featured').count()
        self.vars.update({
            'featured_posts': featured_posts,
            'total_count': total_count,
            'page': page,
            'per_page': per_page,
        })
        self.render('featured_posts/index.html', **self.vars)
