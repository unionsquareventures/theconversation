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

        try:
            q_number = self.get_argument('question_number')
            secondary_id = 'question' + str(int(q_number))
        except:
            a_number = self.get_argument('annotation_number')
            secondary_id = 'annotation' + str(int(a_number))

        self.vars.update({
            'post': post,
            'secondary_id': secondary_id,
        })
        self.render('disqus/index.html', **self.vars)

