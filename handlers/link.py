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
import os
from lib.sanitize import html_sanitize, linkify
from lib.hackpad import HackpadAPI
from base import BaseHandler
import mongoengine
from models import Link, User, Question, Tag, Post, Content

from urlparse import urlparse
from BeautifulSoup import BeautifulSoup

class LinkHandler(BaseHandler):
    def __init__(self, *args, **kwargs):
        super(LinkHandler, self).__init__(*args, **kwargs)

    def index(self):
        # list posts
        query = {}
        tag = self.get_argument('tag', '')
        if tag:
            query.update({
                'tags': tag,
            })
        ordering = {
            'hot': ('-votes', '-date_created'),
            'new': ('-date_created', '-votes')
        }
        sort_by = self.get_argument('sort_by', 'hot')
        posts = Content.objects(featured=False, deleted=False, **query).order_by(*ordering[sort_by])
        featured_posts = list(Content.objects(featured=True, deleted=False).order_by('-date_created'))

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
            'featured_posts': featured_posts,
            'tags': tags,
            'current_tag': tag,
            'urlparse': urlparse,
        })
        self.render('links/index.html', **self.vars)

    def detail(self, id):
        link = Link.objects(id=id).first()
        if not link:
            raise tornado.web.HTTPError(404)
        if link.deleted:
            self.write("Deleted.")
            return
        if link.url:
            link.url_domain = urlparse(link.url).netloc
        self.vars.update({'link': link})
        self.render('links/get.html', **self.vars)

    @tornado.web.asynchronous
    def new(self, model=Link(), errors={}):
        hackpad_api = HackpadAPI(settings.hackpad['oauth_client_id'],
                                            settings.hackpad['oauth_secret'],
                                            domain=settings.hackpad['domain'])
        def hpad_created(hpad_json):
            model.hackpad_url = 'https://%s.hackpad.com/%s'\
                                            % (settings.hackpad['domain'], hpad_json['padId'])
            # Link creation page
            self.vars.update({
                'model': model,
                'errors': errors,
            })
            self.render('links/new.html', **self.vars)

        hackpad_api.create(hpad_created)


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
        body_raw = attributes.get('body_raw', '')
        body_html = html_sanitize(body_raw)

        # Handle Hackpad
        if attributes.get('has_hackpad'):
            attributes['has_hackpad'] = True

        attributes.update({
            'user': User(**self.get_current_user()),
            'body_html': body_html,
            'featured': True if attributes.get('featured') else False,
            'tags': tag_names,
        })

        link = Link(**attributes)
        try:
            link.save()
        except mongoengine.ValidationError, e:
            self.new(model=link, errors=e.errors)
            return

        self.redirect('/links/%s' % link.id)

    def update(self, id):
        link = Link.objects(id=id).first()
        if not link:
            raise tornado.web.HTTPError(404)

        if not self.get_current_user()['username'] == link.user['username']:
            raise tornado.web.HTTPError(401)

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
        body_raw = attributes.get('body_raw', '')
        body_html = html_sanitize(body_raw)

        # Handle Hackpad
        if attributes.get('has_hackpad'):
            attributes['has_hackpad'] = True

        attributes.update({
            'user': User(**self.get_current_user()),
            'body_html': body_html,
            'featured': True if attributes.get('featured') else False,
            'tags': tag_names,
        })

        if attributes['_xsrf']:
            del attributes['_xsrf']

        attributes = {('set__%s' % k): v for k, v in attributes.iteritems()}
        link.update(**attributes)
        try:
            link.save()
        except mongoengine.ValidationError, e:
            self.edit(link.id, errors=e.errors)
            return

        self.redirect('/links/%s' % link.id)

    def edit(self, id, errors={}):
        link = Link.objects(id=id).first()
        if not link:
            raise tornado.web.HTTPError(404)

        if not self.get_current_user()['username'] == link.user['username']:
            raise tornado.web.HTTPError(401)

        # Link modification page
        self.vars.update({
            'model': link,
            'errors': errors,
        })
        self.render('links/new.html', **self.vars)


    @tornado.web.authenticated
    def get(self, id='', action=''):
        if action == 'upvote' and id:
            self.upvote(id)
        else:
            super(LinkHandler, self).get(id, action)

    def upvote(self, id):
        username = self.get_current_user()['username']
        user_q = {'$elemMatch': {'username': username}}
        link = Link.objects(id=id).fields(voted_users=user_q).first()
        if not link:
            raise tornado.web.HTTPError(404)
        detail = self.get_argument('detail', '')
        if link.voted_users:
            self.redirect(('/links/%s?error' % link.id) if detail else '/posts?error')
            return


        link.update(inc__votes=1)
        link.update(push__voted_users=User(**self.get_current_user()))

        self.redirect(('/links/%s' % link.id) if detail else '/posts')
