import settings
import tornado.web
import tornado.auth
import tornado.httpserver
import os
import lib.sanitize as sanitize
from base import BaseHandler
import mongoengine
from models import Tag, Post, UserInfo, User, VotedUser

from urlparse import urlparse
from datetime import datetime
import datetime as dt
import time

class PostHandler(BaseHandler):
    def __init__(self, *args, **kwargs):
        super(PostHandler, self).__init__(*args, **kwargs)

    def index(self):
        # list posts
        query = {}
        tag = self.get_argument('tag', '').lower()
        if tag:
            query.update({
                'tags': tag,
            })
        per_page = 20
        sort_by = self.get_argument('sort_by', 'hot')
        if not sort_by in ['hot', 'new']:
            raise tornado.web.HTTPError(400)

        anchor = self.get_argument('anchor', None)
        action = self.get_argument('action', '')
        count = int(self.get_argument('count', 0))
        if count < 0:
            count = 0

        original_count = count
        if action == 'before':
            count += per_page

        page = 1
        featured_posts = list(Post.objects(featured=True, deleted=False, **query).order_by('-date_featured')[:5])
        lua = "local num_posts = redis.call('ZCARD', '{sort_by}')\n"
        if anchor != None:
            anchor = Post.objects(id=anchor).first()
            if not anchor:
                raise tornado.web.HTTPError(400)
            if anchor.featured:
                lua += "local rank = {count}\n"
            else:
                lua += "local rank = redis.call('ZREVRANK', '{sort_by}', '{anchor.id}')\n"
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
        posts = {str(p.id): p for p in posts}
        posts = [posts[id] for id in ordered_ids]

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
            'count': original_count,
            'action': action,
        })
        self.render('post/index.html', **self.vars)

    def detail(self, id):
        post = Post.objects(slugs=id).first()
        if not post:
            raise tornado.web.HTTPError(404)
        self.vars.update({'post': post})
        if post.deleted:
            self.render('post/deleted.html', **self.vars)
            return
        self.render('post/get.html', **self.vars)

    @tornado.web.asynchronous
    def new(self, post=None, errors={}):
        if post == None:
            post = Post()
            post.url = self.get_argument('url', '')
            post.title = self.get_argument('title', '')

        # Link creation page
        self.vars.update({
            'post': post,
            'errors': errors,
            'edit_mode': False,
        })
        self.render('post/new.html', **self.vars)

    @tornado.web.asynchronous
    def create(self):
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
        body_html = sanitize.html_sanitize(body_raw, media=self.is_admin())
        body_text = sanitize.html_to_text(body_html)
        body_truncated = sanitize.truncate(body_text, 500)

        protected_attributes = ['date_created', '_xsrf', 'user', 'votes', 'voted_users', 'deleted', 'slugs']
        for attribute in protected_attributes:
            if attributes.get(attribute):
                del attributes[attribute]

        featured = False
        date_featured = None
        if self.is_admin() and attributes.get('featured'):
            featured = True
            date_featured = datetime.now()

        date_created = dt.datetime.now()
        user_id_str = self.get_current_user_id_str()
        user_info = UserInfo.objects(user__id_str=user_id_str).first()
        attributes.update({
            'user': user_info.user,
            'body_html': body_html,
            'body_raw': body_raw,
            'body_truncated': body_truncated,
            'body_text': body_text,
            'has_hackpad': True if attributes.get('has_hackpad') else False,
            'featured': featured,
            'date_featured': date_featured,
            'tags': tag_names,
            'date_created': date_created,
            'votes': 1,
            'voted_users': [VotedUser(id=user_id_str)]
        })

        post = Post(**attributes)
        try:
            if self.is_admin():
                post.save()
            else:
                post.save(body_length_limit=settings.post_char_limit)
        except mongoengine.ValidationError, e:
            self.new(post=post, errors=e.errors)
            return
        redis = self.settings['redis']
        redis.set('post:%s:votes' % post.id, 1)
        self.redis_add(post)
        sendgrid = self.settings['sendgrid']
        if post.url:
            subject = '%s shared a link on USV.com' % post.user['username']
        else:
            subject = '%s wrote a new post on USV.com' % post.user['username']
        text = '"%s" submitted by %s. Read it here: http://%s/posts/%s'\
                        % (post.title, post.user['username'],
                                        settings.base_url, post.slug)
        for user_id, address in settings.admin_user_emails.iteritems():
            if user_id == post.user['id_str']:
                continue
            print 'sending to %s' % address
            sendgrid.send_email(lambda x: None, **{
                'from': 'web@usv.com',
                'to': address,
                'subject': subject,
                'text': text,
            })
        self.redirect('/posts/%s' % post.slug)

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
        lua += "redis.call('ZADD', 'hot', score, '{post.id}')\n"
        lua = lua.format(post=post, base_score=base_score)
        incr_score = redis.register_script(lua)
        incr_score()

    def update(self, id):
        post = Post.objects(slugs=id).first()
        if not post:
            raise tornado.web.HTTPError(404)

        id_str = self.get_current_user_id_str()
        op_rights = (id_str == post.user['id_str']) and not post.deleted
        if not (self.is_admin() or op_rights):
            raise tornado.web.HTTPError(401)

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
        body_html = sanitize.html_sanitize(body_raw, self.is_admin())
        body_text = sanitize.html_to_text(body_html)
        body_truncated = sanitize.truncate(body_text, 500)

        protected_attributes = ['date_created', '_xsrf', 'user', 'votes', 'voted_users', 'slugs']
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
            attributes.update({
                'date_deleted': dt.datetime.now(),
            })
        elif attributes.get('deleted') and post.deleted:
            self.redis_add(post)

        attributes.update({
            'user': post.user,
            'body_html': body_html,
            'body_raw': body_raw,
            'body_truncated': body_truncated,
            'has_hackpad': True if attributes.get('has_hackpad') else False,
            'body_text': body_text,
            'featured': featured,
            'date_featured': date_featured,
            'deleted': True if attributes.get('deleted') else False,
            'tags': tag_names,
        })
        old_title = post.title
        post.set_fields(**attributes)
        try:
            if self.is_admin():
                post.save()
            else:
                post.save(body_length_limit=settings.post_char_limit)
        except mongoengine.ValidationError, e:
            self.edit(post.slug, errors=e.errors)
            return
        self.redirect('/posts/%s' % post.slug)

    def edit(self, id, errors={}):
        post = Post.objects(slugs=id).first()
        if not post:
            raise tornado.web.HTTPError(404)

        id_str = self.get_current_user_id_str()
        op_rights = (id_str == post.user['id_str']) and not post.deleted
        if not (op_rights or self.is_admin()):
            raise tornado.web.HTTPError(401)

        # Modification page
        self.vars.update({
            'post': post,
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
            raise tornado.web.HTTPError(401)
        try:
            post = Post.objects.get(slugs=id)
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
        id_str = self.get_current_user_id_str()
        user_q = {'$elemMatch': {'_id': id_str}}
        post = Post.objects(slugs=id).fields(votes=True, date_created=True,
                                        featured=True, voted_users=user_q).first()
        if not post:
            raise tornado.web.HTTPError(404)
        if post.voted_users and not self.is_admin():
            self.write_json({'error': 'You have already upvoted this post.'})
            return

        post.update(inc__votes=1)
        if not post.voted_users:
            post.update(push__voted_users=VotedUser(id=id_str))

        base_score = time.mktime(post.date_created.timetuple()) / 45000.0
        redis = self.settings['redis']
        lua = "local votes = redis.call('INCR', 'post:{post.id}:votes')\n"
        if not post.featured:
            lua += "votes = math.log10(votes)\n"
            lua += "local score = {base_score} + votes\n"
            lua += "redis.call('ZADD', 'hot', score, '{post.id}')\n"
            lua = lua.format(post=post, base_score=base_score)
        incr_score = redis.register_script(lua)
        incr_score()

        self.write_json({'votes': post.votes + 1})
