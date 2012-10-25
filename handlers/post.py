import settings
import tornado.web
import tornado.auth
import tornado.httpserver
from markdown import markdown
from lib.markdown.mdx_video import VideoExtension
import datetime as dt
import re
from collections import defaultdict
from itertools import groupby
from operator import itemgetter

from base import BaseHandler

import mongoengine
from models import Post, User, Question, Tag

class PostHandler(BaseHandler):
    def __init__(self, *args, **kwargs):
        super(PostHandler, self).__init__(*args, **kwargs)

    def index(self):
        # list posts
        query = {}
        tag = self.get_argument('tag', '')
        if tag:
            query.update({
                'tags': tag,
            })
        posts = Post.objects(featured=False, **query).order_by('-votes')
        featured_posts = Post.objects(featured=True).order_by('-date_created')
        tags = Tag.objects()
        self.vars.update({
            'posts': posts,
            'featured_posts': featured_posts,
            'tags': tags,
            'current_tag': tag,
            'user': self.get_current_user(),
        })
        self.render('posts/index.html', **self.vars)

    def detail(self, id):
        post = Post.objects(id=id).first()
        if not post:
            raise tornado.web.HTTPError(404)
        self.vars.update({'post': post})
        self.render('posts/get.html', **self.vars)

    @tornado.web.authenticated
    def new(self, model=Post(), errors={}):
        # Create a post
        self.vars.update({
            'model': model,
            'post_id': '',
            'errors': errors,
        })
        self.render('posts/new.html', **self.vars)

    @tornado.web.authenticated
    def create(self):
        attributes = {k: v[0] for k, v in self.request.arguments.iteritems()}

        # Handle tags
        tag_names = attributes.get('tags', '').split(',')
        tag_names = [t.strip() for t in tag_names]
        tag_names = [t for t in tag_names if t]
        exising_names = [t.name for t in Tag.objects(name__in=tag_names)]
        for name in tag_names:
            if name in exising_names:
                continue
            tag = Tag(name=name)
            tag.save()

        # Content
        video_ext = VideoExtension(configs={})
        body_raw = attributes.get('body_raw', '')
        body_html = markdown(body_raw, extensions=[video_ext],
                                    output_format='html5', safe_mode=False)

        attributes.update({
            'user': User(**self.get_current_user()),
            'body_html': body_html,
            'featured': True if attributes.get('featured') else False,
            'tags': tag_names,
        })

        post = Post(**attributes)
        try:
            post.save()
        except mongoengine.ValidationError, e:
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

        self.redirect('/posts/%s' % post.id)

    # Update a post
    @tornado.web.authenticated
    def edit(self, id):
        id = id
        post = Post.objects(id=id).first()
        if not post:
            raise tornado.web.HTTPError(404)

        self.vars.update({
            'model':  post,
            'post_id': post.id,
        })
        self.render('posts/new.html', **self.vars)

    @tornado.web.authenticated
    def update(self, id):
        pass

    def get(self, id='', action=''):
        if action == 'upvote' and id:
            self.upvote(id)
        else:
            super(PostHandler, self).get(id, action)

    @tornado.web.authenticated
    def upvote(self, id):
        username = self.get_current_user()['username']
        user_q = {'$elemMatch': {'username': username}}
        post = Post.objects(id=id).fields(voted_users=user_q).first()
        if not post:
            raise tornado.web.HTTPError(404)
        if post.voted_users:
            self.redirect('/posts?error')
            return
        post.update(inc__votes=1)
        post.update(push__voted_users=User(**self.get_current_user()))
        self.redirect('/posts')
