import settings
import tornado.web
import tornado.auth
import tornado.httpserver
import datetime as dt
import json

from base import BaseHandler
from models import Post, Annotation, AnnotationRange

# TODO: Annotation authentication and xsrf cookies

class AnnotationHandler(BaseHandler):

    def index(self):
        post_id = int(self.get_argument('post_id'))
        post = Post.objects(id=post_id).first()
        if not post:
            raise tornado.web.HTTPError(404)
        annotations = []
        for c in range(len(post.annotations)):
            a = post.annotations[c].to_mongo()
            a.update({
                'id': "%i_%i" % (post.id, c),
            })
            annotations.append(a)

        self.render_json({
            'total': len(annotations),
            'rows': annotations,
        })

    def detail(self, id):
        ids = id.split('_')
        post_id = int(ids[0])
        annotation_num = int(ids[1])

        post = Post.objects(id=post_id).first()
        if not post:
            raise tornado.web.HTTPError(404)
        a = annotation[annotation_num]
        a['id'] = id
        self.render_json(a.to_mongo())

    def create(self):
        req = json.loads(self.request.body)
        req['post_id'] = int(req['post_id'])
        post_id = int(req['post_id'])

        post = Post.objects(id=post_id).first()
        if not post:
            raise tornado.web.HTTPError(404)

        annotation_num = len(post.annotations)
        a = Annotation(**req)
        post.update(push__annotations=a)

        a = a.to_mongo()
        a['id'] = '%i_%i' % (post_id, annotation_num)
        self.render_json(a)

    def delete(self, id):
        ids = id.split('_')
        post_id = int(params[0])
        annotation_num = int(params[1])

        post = Post.objects(id=post_id).first()
        if not post:
            raise tornado.web.HTTPError(404)

        post.update({'unset__annotations.%s' % (annotation_num) : 1})
        post.update('pull__annotations'==0)

        return

    def update(self, id):
        pass

    def check_xsrf_cookie(self):
        pass
