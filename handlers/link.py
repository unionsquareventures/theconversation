import settings
import tornado.web
import tornado.auth
import tornado.httpserver
import os
from lib.sanitize import html_sanitize, linkify
from base import BaseHandler
import mongoengine
from models import Link, User, Tag, Content

from urlparse import urlparse
from BeautifulSoup import BeautifulSoup

class LinkHandler(BaseHandler):
    def __init__(self, *args, **kwargs):
        super(LinkHandler, self).__init__(*args, **kwargs)

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
        # Link creation page
        self.vars.update({
            'model': model,
            'errors': errors,
            'edit_mode': False,
        })
        self.render('links/new.html', **self.vars)

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

        attributes.update({
            'user': User(**self.get_current_user()),
            'featured': False,
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
        tag_names = [t.strip().lower() for t in tag_names]
        tag_names = [t for t in tag_names if t]
        exising_names = [t.name for t in Tag.objects(name__in=tag_names)]
        for name in tag_names:
            if name in exising_names:
                continue
            tag = Tag(name=name)
            tag.save()

        attributes.update({
            'user': User(**self.get_current_user()),
            'featured': False,
            'tags': tag_names,
        })

        protected_attributes = ['_xsrf', 'user', 'votes', 'voted_users']
        for attribute in protected_attributes:
            if attributes.get('attribute'):
                del attributes[attribute]

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
            'edit_mode': True,
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
            self.redirect(('/links/%s?error' % link.id) if detail else '/?error')
            return

        link.update(inc__votes=1)
        link.update(push__voted_users=User(**self.get_current_user()))

        self.redirect(('/links/%s' % link.id) if detail else '/')
