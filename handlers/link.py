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
        links = Content.objects(featured=False, **query).order_by('-votes', '-date_created')
        # ^ Also could be Content.objects
        tags = Tag.objects()
        self.vars.update({
            'links': links,
            'tags': tags,
            'current_tag': tag,
        })
        self.render('links/index.html', **self.vars)

    def detail(self, id):
        link = Link.objects(id=id).first()
        if not link:
            raise tornado.web.HTTPError(404)
        self.vars.update({'link': link})
        self.render('links/get.html', **self.vars)

    @tornado.web.authenticated
    def new(self, model=Link(), errors={}):
        # Create a link
        self.vars.update({
            'model': model,
            'link_id': '',
            'errors': errors,
        })
        self.render('links/new.html', **self.vars)

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

        link = Link(**attributes)
        try:
            link.save()
        except mongoengine.ValidationError, e:
            self.new(model=link, errors=e.errors)
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
            link.update(push__questions=q)

        # Generate thumbnail
        thumb_path = "static/images/link_thumbnails/%s.png" % str(link.id)
        thumb_path = os.path.join(settings.PROJECT_ROOT,  thumb_path)
        script_path = os.path.join(settings.PROJECT_ROOT, "scripts/rasterize.js")

        def generate_thumb(*args):
            subprocess.call(['/usr/bin/phantomjs'] + list(args))

        p = Process(target=generate_thumb, args=(script_path, link.url, thumb_path))
        p.start()

        self.redirect('/links/%s' % link.id)

    @tornado.web.authenticated
    def update(self, id):
        pass

    def get(self, id='', action=''):
        if action == 'upvote' and id:
            self.upvote(id)
        else:
            super(LinkHandler, self).get(id, action)

    @tornado.web.authenticated
    def upvote(self, id):
        username = self.get_current_user()['username']
        user_q = {'$elemMatch': {'username': username}}
        link = Link.objects(id=id).fields(voted_users=user_q).first()
        if not link:
            raise tornado.web.HTTPError(404)
        if link.voted_users:
            self.redirect('/links?error')
            return
        link.update(inc__votes=1)
        link.update(push__voted_users=User(**self.get_current_user()))
        self.redirect('/links')
