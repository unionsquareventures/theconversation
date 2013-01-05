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
from lib.sanitize import html_sanitize
from base import BaseHandler

import mongoengine
from models import Link, User, Question, Tag, Post, Content

import subprocess
from multiprocessing import Process

class LinkHandler(BaseHandler):
    def __init__(self, *args, **kwargs):
        super(LinkHandler, self).__init__(*args, **kwargs)

    def index(self):
        # list posts
        query = {
        }
        tag = self.get_argument('tag', '')
        if tag:
            query.update({
                'tags': tag,
            })
        links = Content.objects(**query).order_by('-votes', '-date_created')
        # ^ Also could be Content.objects
        tags = Tag.objects()
        self.vars.update({
            'links': links,
            'tags': tags,
            'current_tag': tag,
            "test": {"a": "one"},
        })
        self.render('links/index.html', **self.vars)

    def detail(self, id):
        link = Link.objects(id=id).first()
        if not link:
            raise tornado.web.HTTPError(404)
        self.vars.update({'link': link})
        self.render('links/get.html', **self.vars)

    def new(self, model=Link(), errors={}):
        # Create a link
        self.vars.update({
            'model': model,
            'link_id': '',
            'errors': errors,
        })
        self.render('links/new.html', **self.vars)

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
            #attributes['hackpad_id'] =

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
        pass

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
