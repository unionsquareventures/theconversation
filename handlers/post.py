import settings
import tornado.web
import tornado.auth
import tornado.httpserver
from markdown import markdown
from lib.markdown.mdx_video import VideoExtension
import datetime as dt
import re
from collections import defaultdict

from base import BaseHandler
from minifier import Minifier

import mongoengine
from models import Post, User, Question

minifier = Minifier()

class PostHandler(BaseHandler):
    def __init__(self, *args, **kwargs):
        super(PostHandler, self).__init__(*args, **kwargs)
        self.vars['minifier'] = minifier

    def index(self):
        # list posts
        self.vars.update({'posts': Post.objects.all().order_by('date_created')})
        self.render('posts/index.html', **self.vars)

    def detail(self, id):
        id = minifier.base62_to_int(id)
        post = Post.objects(id=id).first()
        if not post:
            raise tornado.web.HTTPError(404)
        self.vars.update({'post': post})
        self.render('posts/get.html', **self.vars)

    # Create a post
    @tornado.web.authenticated
    def new(self, model=Post(), errors={}):
        self.vars.update({
            'model': model,
            'post_id': '',
            'errors': errors,
        })
        self.render('posts/new.html', **self.vars)

    @tornado.web.authenticated
    def post(self, params=''):
        if params:
            self.put(params)
            return
        ##
        attributes = {k: v[0] for k, v in self.request.arguments.iteritems()}
        video_ext = VideoExtension(configs={})
        body_raw = attributes.get('body_raw', '')
        body_html = markdown(body_raw, extensions=[video_ext], output_format='html5', safe_mode=False)
        attributes.update({
            'user': User(**self.get_current_user()),
            'body_html': body_html,
        })
        post = Post(**attributes)
        try:
            post.save()
        except mongoengine.ValidationError, e:
            print e
            self.new(model=post, errors=e.errors)
            return

        # Obtain questions
        questions_data = defaultdict(dict)
        for key, value in attributes.iteritems():
            if not key.startswith('question['):
                continue
            m = re.search(r"question\[([0-9]+)\]\[([A-z0-9\_]+)\]", key)
            index = int(m.group(1))
            field = m.group(2)
            questions_data[index][field] = value

        # Create questions
        for q in questions_data.values():
            # Ignore empty questions
            if not q["text"]:
                continue
            q = Question(**q)
            post.update(push__questions=q)

        self.redirect('/posts/%s' % minifier.int_to_base62(post.id))

    # Update a post
    @tornado.web.authenticated
    def edit(self, id):
        id = minifier.base62_to_int(id)
        post = Post.objects(id=id).first()
        if not post:
            raise tornado.web.HTTPError(404)

        self.vars.update({
            'model':  post,
            'post_id': post.minified_id(),
        })
        self.render('posts/new.html', **self.vars)


    @tornado.web.authenticated
    def put(self, id=''):
        id = minifier.base62_to_int(id)
        post = Post.objects(id=id).first()
        if not post:
            raise tornado.web.HTTPError(404)
        #
        attributes = {k: v[0] for k, v in self.request.arguments.iteritems()}
        del attributes['_xsrf']
        video_ext = VideoExtension(configs={})
        body_html = markdown(attributes['body_raw'], extensions=[video_ext], output_format='html5', safe_mode=False)
        attributes.update({
            'user': User(**self.get_current_user()),
            'body_html': body_html,
        })
        attributes = {'set__'+k: v for k, v in attributes.iteritems()}
        post.update(**attributes)
        try:
            post.save()
        except mongoengine.ValidationError, e:
            self.new(model=post, errors=e.errors)
            return
        self.redirect('/posts/%s' % post.minified_id())

