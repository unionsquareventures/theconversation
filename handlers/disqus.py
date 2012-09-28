import settings
import tornado.web
import tornado.auth
import tornado.httpserver

from base import BaseHandler
from models import Post

class DisqusHandler(BaseHandler):

    def get(self):
        post = Post.objects(id=self.get_argument('post_id')).first()
        if not post:
            raise tornado.web.HTTPError(404)
        question_number = int(self.get_argument('question_number'))

        self.vars.update({
            'post': post,
            'question_number': question_number,
        })
        self.render('disqus/index.html', **self.vars)

