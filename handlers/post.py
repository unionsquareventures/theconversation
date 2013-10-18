import settings
import tornado.web
import tornado.auth
import tornado.escape
import tornado.httpserver
from tornado.httpclient import *
import os
import lib.sanitize as sanitize
from base import BaseHandler
import mongoengine
from models import Tag, Post, UserInfo, User, VotedUser
import json
from urlparse import urlparse
from datetime import datetime
import datetime as dt
import time
import re
import urllib

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
        sort_by_specified = self.get_argument('sort_by', '')
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
        
        sticky = Post.objects(slug="welcome-to-the-new-usvcom")
        featured_posts = list(Post.objects(featured=True, deleted=False, slug__ne="welcome-to-the-new-usvcom", **query).order_by('-date_created')[:6])
        
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
            'sort_by_specified': sort_by_specified,
            'posts': posts,
            'page': page,
            'per_page': per_page,
            'featured_posts': featured_posts,
            'sticky': sticky,
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
        author = UserInfo.objects(user__username=post.user.username).first()
        sso = self.settings['disqus'].get_sso(True, {})
        id_str = self.get_current_user_id_str()
        u = None
        if id_str:
            u = UserInfo.objects.get(user__id_str=id_str)
            if u.email_address:
                user_url = 'http://www.twitter.com/%s' % u.user.screen_name
                user_info = {
                        'id': id_str,
                        'username': u.user.username,
                        'email': u.email_address,
                        'avatar': u.user.profile_image_url,
                        'url': user_url,
                }
                sso = self.settings['disqus'].get_sso(True, user_info)
        self.vars.update({
            'post': post,
            'disqus_sso': sso,
            'urlparse': urlparse,
            'user_info': u,
            'subscribe': self.get_argument('subscribe', ''),
            'author': author
        })
        if post.deleted:
            self.render('post/deleted.html', **self.vars)
            return
        if post.featured:
            self.render("post/get-featured.html", **self.vars)
            return
        self.render('post/get.html', **self.vars)

    @tornado.web.authenticated
    @tornado.web.asynchronous
    def new(self, post=None, errors=None, existing_posts=None):
        if self.is_blacklisted(self.get_current_username()):
            self.vars.update({
                'banned': True
            })
        else:
            self.vars.update({
                'banned': False
            })
        
        if not errors:
            errors = {}

        if post == None:
            post = Post()
            post.title = self.get_argument('title', '')
            post.url = self.get_argument('url', '')
            # Check for an existing URL
            normalized_url = post.url
            if normalized_url:
                normalized_url = urlparse(normalized_url)
                netloc = normalized_url.netloc.split('.')
                if netloc[0] == 'www':
                    del netloc[0]
                path = normalized_url.path
                if path and path[-1] == '/':
                    path = path[:-1]
                normalized_url = '%s%s' % ('.'.join(netloc), path)
                post.normalized_url = normalized_url
                posts = Post.objects(normalized_url=normalized_url, deleted=False)[:5]
                if posts:
                    existing_posts = posts

        # Link creation page
        self.vars.update({
            'post': post,
            'errors': errors,
            'edit_mode': False,
            'existing_posts': existing_posts,
        })
        self.render('post/new.html', **self.vars)

    @tornado.web.authenticated
    @tornado.web.asynchronous
    def create(self):
        attributes = {k: v[0] for k, v in self.request.arguments.iteritems()}

        # Handle tags
        tag_names = attributes.get('tags', '').split(',')
        tag_names = [t.strip().lower() for t in tag_names]
        tag_names = [t for t in tag_names if t]
        existing_names = [t.name for t in Tag.objects(name__in=tag_names)]
        for name in tag_names:
            if name in existing_names:
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
        u = UserInfo.objects(user__id_str=user_id_str).first()
        attributes.update({
            'title': unicode(attributes['title'].decode('utf-8')),
            'user': u.user,
            'normalized_url': '',
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

        # Check for an existing URL
        normalized_url = attributes.get('url', '')
        if normalized_url:
            normalized_url = urlparse(normalized_url)
            netloc = normalized_url.netloc.split('.')
            if netloc[0] == 'www':
                del netloc[0]
            path = normalized_url.path
            if path and path[-1] == '/':
                path = path[:-1]
            normalized_url = '%s%s' % ('.'.join(netloc), path)
            post.normalized_url = normalized_url
            if not self.get_argument('bypass_dup_check', ''):
                posts = Post.objects(normalized_url=normalized_url, deleted=False)[:5]
                if posts:
                    self.new(post=post, existing_posts=posts)
                    return

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

        post_url = '/posts/%s' % post.slug
        subscribe_param = ''
        if not u.email_address:
            subscribe_param = '?subscribe=true'

        # Attempt to create the post's thread
        user_url = 'http://www.twitter.com/%s' % u.user.screen_name
        user_info = {
                'id': u.user.id_str,
                'username': u.user.username,
                'email': u.email_address,
                'avatar': u.user.profile_image_url,
                'url': user_url,
        }
        # Subscribe the OP to the thread
        disqus = self.settings['disqus']
        def _created(response):
            if not response:
                return
            thread_id = response['id']
            
            thread_info.update({
                'disqus_id': thread_id
            })
            
            def _posted(response):
                return
            #leave post as comment.
            #disqus.post_comment(_posted, user_info, thread_info)
            
            #subscribe user to thread
            disqus.subscribe(lambda x: None, user_info, thread_id)
            
            
        thread_info = {
                'title': post.title.encode('utf-8'),
                'identifier': post.id,
        }
        disqus.create_thread(_created, user_info, thread_info)
        
        
        
        # Don't send an email if not a USVer
        if not self.is_admin():
            self.redirect('/posts/%s%s' % (post.slug, subscribe_param))
            return


         # Z trying to modify emails. 
        try:
            print "----------------------------------------------"
            print "Trying new email"
            print "----------------------------------------------"
            sendgrid = self.settings['sendgrid']
            subject = 'USV.com: %s posted "%s"' % (post.user['username'], post.title)
            if post.url: # post.url is the link to external content (if any)
                post_link = 'External Link: %s \n\n' % post.url
            else:
                post_link = ''
            post_url = "http://%s/posts/%s" % (settings.base_url, post.slug)
            print post_url
            text = '"%s" ( %s ) posted by %s. \n\n %s %s'\
                            % (post.title.encode('ascii', errors='ignore'), post_url, 
                                post.user['username'].encode('ascii', errors='ignore'), post.link, post.body_html)

            print text
            for user_id, address in settings.admin_user_emails.iteritems():
                if user_id == post.user['id_str']:
                    continue
                sendgrid.send_email(lambda x: None, **{
                    'from': 'web@usv.com',
                    'to': address,
                    'subject': subject,
                    'text': text,
                })
            self.redirect('/posts/%s%s' % (post.slug, subscribe_param))
        except: 
            # Send email to USVers if OP is USV
            sendgrid = self.settings['sendgrid']
            if post.url:
                subject = '%s shared a link on USV.com' % post.user['username']
            else:
                subject = '%s wrote a new post on USV.com' % post.user['username']
            if post.url:
                relation = 'shared'
                post_link = '( %s )' % post.url
            else:
                relation = 'written'
                post_link = ''
            text = '"%s" %s %s by %s. \n\nOn USV.com: http://%s/posts/%s'\
                            % (post.title.encode('ascii', errors='ignore'), post_link,
                                    relation, post.user['username'].encode('ascii', errors='ignore'),
                                            settings.base_url, post.slug)
            for user_id, address in settings.admin_user_emails.iteritems():
                if user_id == post.user['id_str']:
                    continue
                sendgrid.send_email(lambda x: None, **{
                    'from': 'web@usv.com',
                    'to': address,
                    'subject': subject,
                    'text': text,
                })
            self.redirect('/posts/%s%s' % (post.slug, subscribe_param))
        
       
        
    
    @tornado.web.authenticated
    def bumpup(self, id):
        post = Post.objects(slugs=id).first()
        
        if not post:
            raise tornado.web.HTTPError(404)
            
        if not self.is_staff(self.get_current_username()):
            raise tornado.web.HTTPError(401)
        
        else:
            self.redis_incrby(post, 0.25)
            self.redirect('/')
    
    @tornado.web.authenticated
    def bumpdown(self, id):
        post = Post.objects(slugs=id).first()
        
        if not post:
            raise tornado.web.HTTPError(404)
            
        if not self.is_staff(self.get_current_username()):
            raise tornado.web.HTTPError(401)
        
        else:
            self.redis_incrby(post, -0.25)
            self.redirect('/')
    
    @tornado.web.authenticated
    def mute(self, id):
        post = Post.objects(slugs=id).first()
        
        if not post:
            raise tornado.web.HTTPError(404)
            
        if not self.is_staff(self.get_current_username()):
            raise tornado.web.HTTPError(401)
        
        else:
            post.update(set__muted=True)
            #redis = self.settings['redis']
            #redis.zrem('hot', post.id)
            self.redirect('/')
            
    @tornado.web.authenticated
    def unmute(self, id):
        post = Post.objects(slugs=id).first()
        
        if not post:
            raise tornado.web.HTTPError(404)
            
        if not self.is_staff(self.get_current_username()):
            raise tornado.web.HTTPError(401)
        
        else:
            post.update(set__muted=False)
            #redis = self.settings['redis']
            #redis.zrem('hot', post.id)
            self.redirect('/')

    def redis_remove(self, post):
        redis = self.settings['redis']
        redis.zrem('hot', post.id)
        redis.zrem('new', post.id)

    def redis_add(self, post):
        redis = self.settings['redis']
        redis.zadd('new', time.mktime(post.date_created.timetuple()), post.id)
        
        # change if this person is staff they automatically get to the front page
        # everyone else needs 3 votes
        #if self.is_staff(self.get_current_username()):
        base_score = time.mktime(post.date_created.timetuple()) / 45000.0
        lua = "local votes = redis.call('GET', 'post:{post.id}:votes')\n"
        lua += "votes = math.log10(votes)\n"
        lua += "local score = {base_score} + votes\n"
        lua += "redis.call('ZADD', 'hot', score, '{post.id}')\n"
        lua = lua.format(post=post, base_score=base_score)
        incr_score = redis.register_script(lua)
        incr_score()
        
    def redis_incrby(self, post, increment = 1):
        redis = self.settings['redis']
        lua = "redis.call('ZINCRBY', 'hot', {increment}, '{post.id}')\n"
        lua = lua.format(post=post, increment=increment)
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
        existing_names = [t.name for t in Tag.objects(name__in=tag_names)]
        for name in tag_names:
            if name in existing_names:
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

        normalized_url = attributes.get('url', '')
        if normalized_url:
            normalized_url = urlparse(normalized_url)
            netloc = normalized_url.netloc.split('.')
            if netloc[0] == 'www':
                del netloc[0]
            path = normalized_url.path
            if path and path[-1] == '/':
                path = path[:-1]
            normalized_url = '%s%s' % ('.'.join(netloc), path)

        attributes.update({
            'title': unicode(attributes['title'].decode('utf-8')),
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
            'normalized_url': normalized_url,
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

    @tornado.web.authenticated
    def edit(self, id, errors=None):
        post = Post.objects(slugs=id).first()
        if not post:
            raise tornado.web.HTTPError(404)

        if not errors:
            errors = {}

        id_str = self.get_current_user_id_str()
        op_rights = (id_str == post.user['id_str']) and not post.deleted
        if not (op_rights or self.is_staff(self.get_current_username())):
            raise tornado.web.HTTPError(401)

        # Modification page
        self.vars.update({
            'post': post,
            'errors': errors,
            'edit_mode': True,
            'existing_posts': None,
            'banned': False
        })
        self.render('post/new.html', **self.vars)


    def get(self, id='', action='', tag=''):
        if tag:
            self.show_tag(tag)
        if self.request.path == '/feed':
            self.feed()
        if action == 'edit' and id:
            self.edit(id)
        if action == 'bumpup' and id:
            self.bumpup(id)
        if action == 'bumpdown' and id:
            self.bumpdown(id)
        if action == 'mute' and id:
            self.mute(id)
        if action == 'unmute' and id:
            self.unmute(id)
        if action == 'upvote' and id:
            self.upvote(id)
        if action == 'feature' and id:
            self.feature(id)
        else:
            super(PostHandler, self).get(id, action)
            
    def feed(self):
        posts = Post.objects().order_by('-date_created')[:20]
        self.vars.update({
            'posts': posts
        })
        self.render('post/feed.xml', **self.vars)

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

    def upvote(self, id):
        if not self.get_current_user():
            self.write_json({'error': 'You must be logged in to upvote.', 'redirect': True})
            return
        id_str = self.get_current_user_id_str()
        user_q = {'$elemMatch': {'_id': id_str}}
        post = Post.objects(slugs=id).fields(votes=True, date_created=True,
                                        featured=True, voted_users=user_q).first()
        if not post:
            raise tornado.web.HTTPError(404)
        if post.voted_users and not self.is_staff(self.get_current_username()):
            self.write_json({'error': 'You have already upvoted this post.'})
            return

        # Increment the vote count
        post.update(inc__votes=1)
        if not post.voted_users:
            post.update(push__voted_users=VotedUser(id=id_str))

        base_score = time.mktime(post.date_created.timetuple()) / 45000.0
        redis = self.settings['redis']
        lua = "local votes = redis.call('INCR', 'post:{post.id}:votes')\n"
        if not post.featured and post.votes > 0:
            lua += "votes = math.log10(votes)\n"
            lua += "local score = {base_score} + votes\n"
            lua += "redis.call('ZADD', 'hot', score, '{post.id}')\n"
            lua = lua.format(post=post, base_score=base_score)
        incr_score = redis.register_script(lua)
        incr_score()

        self.write_json({'votes': post.votes + 1})
    
    def show_tag(self, tag):
        # Ensure there is a full text index
        db = Post._get_db()
        query = self.get_argument('query', '')
        #tag = self.get_argument('tag', '')
        if 'author' is self.request.arguments:
            author = self.get_argument('author')
            
        if not (query or tag):
            self.vars.update({
                'query': '',
                'tag': '',
                'total_count': 0,
            })
            self.render('search/index.html', **self.vars)
            return
        page = abs(int(self.get_argument('page', '1')))
        per_page = abs(int(self.get_argument('per_page', '10')))
 
        if 'author' in self.request.arguments and self.get_argument('author') == 'usv':
            results = Post.objects(user__username__in=settings.staff_twitter_handles, deleted=False, tags__in=[tag]).order_by('-date_created')
        else:
            results = Post.objects(deleted=False, tags__in=[tag])
        total_count = len(results)
        posts = results[(page-1)*per_page:(page-1)*per_page+per_page]
    
        self.vars.update({
            'posts': posts,
            'total_count': total_count,
            'page': page,
            'per_page': per_page,
            'tag': tag,
        })
        self.render('search/index.html', **self.vars)
