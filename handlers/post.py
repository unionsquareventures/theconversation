import settings
import tornado.web
import tornado.auth
import tornado.httpserver
import os
from lib.sanitize import html_sanitize, linkify
from base import BaseHandler
import mongoengine
from models import User, Tag, Post

from urlparse import urlparse
from BeautifulSoup import BeautifulSoup
from datetime import datetime
from lib.recaptcha import RecaptchaMixin
import datetime as dt
import time

class PostHandler(BaseHandler, RecaptchaMixin):
    def __init__(self, *args, **kwargs):
        super(PostHandler, self).__init__(*args, **kwargs)
        self.vars.update({
            'recaptcha_render': self.recaptcha_render,
        })

    def index(self):
        # list posts
        query = {}
        tag = self.get_argument('tag', '').lower()
        if tag:
            query.update({
                'tags': tag,
            })
        per_page = 50
        sort_by = self.get_argument('sort_by', 'hot')
        if not sort_by in ['hot', 'new']:
            raise tornado.web.HTTPError(400)

        anchor = self.get_argument('anchor', None)
        action = self.get_argument('action', '')
        count = int(self.get_argument('count', 0))
        page = 1
        featured_posts = list(Post.objects(featured=True, deleted=False, **query).order_by('-date_featured'))
        lua = "local num_posts = redis.call('ZCARD', '{sort_by}')\n"
        if anchor != None:
            anchor = Post.objects(id=anchor).first()
            if not anchor:
                raise tornado.web.HTTPError(400)
            if anchor.featured:
                lua += "local rank = {count}\n"
            else:
                lua += "local rank = redis.call('ZREVRANK', '{sort_by}', {anchor.id})\n"
                lua += "local rank = rank >= {count} - 1 and rank or {count}\n"
            if action == 'after':
                lua += "local rstart = rank + 1\n"
                lua += "local rend = rank + {per_page}\n"
            else:
                lua += "local rstart = rank - {per_page} >= 0 and rank - {per_page} or 0\n"
                lua += "local rend = rank - 1 >= 0 and rank - 1 or 0\n"
        else:
            lua += "local rank = 0\n"
            lua += "local rstart = 0\n"
            lua += "local rend = {per_page} - 1\n"
        redis = self.settings['redis']
        lua += "local ordered_ids = redis.call('ZREVRANGE', '{sort_by}', rstart, rend)\n"\
               "return {{num_posts, rstart, rend, ordered_ids}}"
        lua = lua.format(per_page=per_page, sort_by=sort_by, anchor=anchor, count=count)
        get_posts = redis.register_script(lua)
        num_posts, rstart, rend, ordered_ids = get_posts()
        posts = Post.objects(id__in=ordered_ids)
        posts = {p.id: p for p in posts}
        posts = [posts[int(id)] for id in ordered_ids]

        for post in featured_posts:
            soup = BeautifulSoup(post['body_html'])
            post['body_html'] = soup.prettify()
            #try:
            #    post['body_html'] = truncate(post['body_html'], 500, ellipsis='...')
            #except:
            #    pass
            #post['body_html'] = html_sanitize_preview(post['body_html'])

        tags = Tag.objects()
        self.vars.update({
            'sort_by': sort_by,
            'posts': posts,
            'page': page,
            'per_page': per_page,
            'featured_posts': featured_posts,
            'tags': tags,
            'current_tag': tag,
            'urlparse': urlparse,
            'anchor': anchor,
            'num_posts': num_posts,
            'rstart': rstart,
            'rend': rend,
            'count': count,
            'action': action,
        })
        self.render('post/index.html', **self.vars)

    def detail(self, id):
        post = Post.objects(id=id).first()
        if not post:
            raise tornado.web.HTTPError(404)
        if post.deleted:
            self.write("Deleted.")
            return
        self.vars.update({'post': post})
        self.render('post/get.html', **self.vars)

    @tornado.web.asynchronous
    def new(self, model=Post(), errors={}, recaptcha_error=False):
        # Link creation page
        self.vars.update({
            'model': model,
            'errors': errors,
            'edit_mode': False,
            'recaptcha_error': recaptcha_error,
        })
        self.render('post/new.html', **self.vars)

    @tornado.web.asynchronous
    def create(self):
        self.recaptcha_validate(self._on_validate)

    def _on_validate(self, recaptcha_response):
        attributes = {k: v[0] for k, v in self.request.arguments.iteritems()}

        # Handle tags
        tag_names = attributes.get('tags', '').split(',')
        tag_names = [t.strip().lower() for t in tag_names]
        tag_names = [t for t in tag_names if t]
        exising_names = [t.name for t in Tag.objects(name__in=tag_names)]
        for name in tag_names:
            if name in exising_names:
                continue
            tag = Tag(name=name)
            tag.save()

        # Content
        body_raw = attributes.get('body_raw', '')
        body_html = html_sanitize(body_raw)

        protected_attributes = ['date_created', '_xsrf', 'user', 'votes', 'voted_users']
        for attribute in protected_attributes:
            if attributes.get(attribute):
                del attributes[attribute]

        featured = False
        date_featured = None
        if self.is_admin() and attributes.get('featured'):
            featured = True
            date_featured = datetime.now()

        date_created = dt.datetime.now()
        attributes.update({
            'user': User(**self.get_current_user()),
            'body_html': body_html,
            'featured': featured,
            'date_featured': date_featured,
            'tags': tag_names,
            'date_created': date_created,
            'votes': 1,
            'voted_users': [User(**self.get_current_user())]
        })

        post = Post(**attributes)
        if not recaptcha_response:
            self.new(model=post, recaptcha_error=True)
            return

        try:
            post.save()
        except mongoengine.ValidationError, e:
            self.new(model=post, errors=e.errors)
            return
        redis = self.settings['redis']
        redis.set('post:%i:votes' % post.id, 1)
        self.redis_add(post)
        self.redirect('/posts/%s' % post.id)

    def redis_remove(self, post):
        redis = self.settings['redis']
        redis.zrem('hot', post.id)
        redis.zrem('new', post.id)

    def redis_add(self, post):
        redis = self.settings['redis']
        redis.zadd('new', time.mktime(post.date_created.timetuple()), post.id)
        base_score = time.mktime(post.date_created.timetuple()) / 45000.0
        lua = "local votes = redis.call('GET', 'post:{post.id}:votes')\n"
        lua += "votes = math.log10(votes)\n"
        lua += "local score = {base_score} + votes\n"
        lua += "redis.call('ZADD', 'hot', score, {post.id})\n"
        lua = lua.format(post=post, base_score=base_score)
        incr_score = redis.register_script(lua)
        incr_score()

    def update(self, id):
        post = Post.objects(id=id).first()
        if not post:
            raise tornado.web.HTTPError(404)

        id_str = self.get_current_user()['id_str']
        if not (self.is_admin() or id_str == post.user['id_str']):
            raise tornado.web.HTTPError(403)

        attributes = {k: v[0] for k, v in self.request.arguments.iteritems()}
        # Handle tags
        tag_names = attributes.get('tags', '').split(',')
        tag_names = [t.strip().lower() for t in tag_names]
        tag_names = [t for t in tag_names if t]
        exising_names = [t.name for t in Tag.objects(name__in=tag_names)]
        for name in tag_names:
            if name in exising_names:
                continue
            tag = Tag(name=name)
            tag.save()

        # Content
        body_raw = attributes.get('body_raw', '')
        body_html = html_sanitize(body_raw)

        protected_attributes = ['date_created', '_xsrf', 'user', 'votes', 'voted_users']
        for attribute in protected_attributes:
            if attributes.get(attribute):
                del attributes[attribute]

        featured = post.featured
        date_featured = post.date_featured
        if self.is_admin() and attributes.get('featured') and not featured:
            featured = True
            date_featured = datetime.now()
            self.redis_remove(post)
        if self.is_admin() and not attributes.get('featured'):
            featured = False
            date_featured = None
            self.redis_add(post)

        if attributes.get('deleted') and not post.deleted:
            self.redis_remove(post)
        elif attributes.get('deleted') and post.deleted:
            self.redis_add(post)

        attributes.update({
            'user': User(**self.get_current_user()),
            'body_html': body_html,
            'featured': featured,
            'date_featured': date_featured,
            'deleted': True if attributes.get('deleted') else False,
            'tags': tag_names,
        })
        post.set_fields(**attributes)
        try:
            post.save()
        except mongoengine.ValidationError, e:
            self.edit(post.id, errors=e.errors)
            return
        self.redirect('/posts/%s' % post.id)

    def edit(self, id, errors={}):
        post = Post.objects(id=id).first()
        if not post:
            raise tornado.web.HTTPError(404)

        id_str = self.get_current_user()['id_str']
        if not (id_str == post.user['id_str'] or self.is_admin()):
            raise tornado.web.HTTPError(403)

        # Modification page
        self.vars.update({
            'model': post,
            'errors': errors,
            'edit_mode': True,
        })
        self.render('post/new.html', **self.vars)


    def get(self, id='', action=''):
        if action == 'upvote' and id:
            self.upvote(id)
        elif action == 'feature' and id:
            self.feature(id)
        else:
            super(PostHandler, self).get(id, action)

    @tornado.web.authenticated
    def feature(self, id):
        if not self.is_admin():
            raise tornado.web.HTTPError(403)
        try:
            post = Post.objects.get(id=id)
        except Post.DoesNotExist:
            raise tornado.web.HTTPError(404)
        if not post.featured:
            post.featured = True
            post.date_featured = datetime.now()
            post.save()
            self.redis_remove(post)
        self.redirect('/')

    @tornado.web.authenticated
    def upvote(self, id):
        id_str = self.get_current_user()['id_str']
        user_q = {'$elemMatch': {'id_str': id_str}}
        post = Post.objects(id=id).fields(voted_users=user_q, votes=True, date_created=True).first()
        if not post:
            raise tornado.web.HTTPError(404)
        detail = self.get_argument('detail', '')
        if post.voted_users and not self.is_admin():
            self.redirect(('/posts/%s?error' % post.id) if detail else '/?error')
            return

        post.update(inc__votes=1)
        if not post.voted_users:
            post.update(push__voted_users=User(**self.get_current_user()))

        base_score = time.mktime(post.date_created.timetuple()) / 45000.0
        redis = self.settings['redis']
        lua = "local votes = redis.call('INCR', 'post:{post.id}:votes')\n"
        lua += "votes = math.log10(votes)\n"
        lua += "local score = {base_score} + votes\n"
        lua += "redis.call('ZADD', 'hot', score, {post.id})\n"
        lua = lua.format(post=post, base_score=base_score)
        incr_score = redis.register_script(lua)
        incr_score()

        if detail:
            self.redirect('/posts/%s' % post.id)
        else:
            sort_by = self.get_argument('sort_by', '')
            anchor = self.get_argument('anchor', '')
            count = self.get_argument('count', '')
            action = self.get_argument('action', '')
            self.redirect('/?sort_by=%s&anchor=%s&count=%s&action=%s'\
                                        % (sort_by, anchor, count, action))

