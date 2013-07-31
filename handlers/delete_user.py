from models.post import Post
from base import BaseHandler
import tornado
import datetime as dt

class DeleteUserHandler(BaseHandler):
    def get(self):
        if not self.is_admin():
            raise tornado.web.HTTPError(401)
        msg = self.get_argument('msg', '')
        self.vars.update({
            'msg': msg,
        })
        self.render('delete_user/index.html', **self.vars)

    def post(self):
        post_id = int(self.get_argument('post_id'))
        post = Post.objects(id=post_id).first()
        if not post:
            msg = "Post not found."
            self.redirect('/delete_user?msg=%s'
                                % tornado.escape.url_escape(msg))
            return
        user_id_str = post.user['id_str']
        posts = Post.objects(user__id_str=user_id_str, deleted=False).fields(id=True)
        count = posts.count()
        ids = [p.id for p in posts]
        posts.update(set__deleted=True, set__date_deleted=dt.datetime.now())
        redis = self.settings['redis']
        redis.zrem('hot', *ids)
        redis.zrem('new', *ids)
        msg = "%i post(s) deleted." % count
        self.redirect('/delete_user?msg=%s'
                                % tornado.escape.url_escape(msg))
