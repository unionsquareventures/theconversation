import settings
import tornado.web
import tornado.auth
import tornado.httpserver
from forms import Form
from wtforms import TextField, TextAreaField, IntegerField
from wtforms.validators import InputRequired
from markdown import markdown
from lib.markdown.mdx_video import VideoExtension
import datetime as dt

from base import BaseHandler
from minifier import Minifier

import mongoengine
from models import Post, User

minifier = Minifier()

class PostHandler(BaseHandler):
    def __init__(self, *args, **kwargs):
        super(PostHandler, self).__init__(*args, **kwargs)
        self.vars['minifier'] = minifier

    def get(self, params=''):
        # TODO: Do this inside the routes w/ kwargs
        if params.find('/') == -1:
            params += '/'
        id, action = params.split('/')
        # Route new, detail, and index
        if id == 'new':
            self.new()
            return
        if id and action == '':
            self.detail(id)
            return
        if action == 'edit':
            self.edit(id)
            return
        self.index()

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
            self.new(model=post, errors=e.errors)
            return

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

