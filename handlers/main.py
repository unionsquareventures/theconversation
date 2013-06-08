import settings
import tornado.web
import tornado.auth
import tornado.httpserver
from base import BaseHandler
import mongoengine
from models import Link, User, Tag, Content
from BeautifulSoup import BeautifulSoup
from urlparse import urlparse

class MainHandler(BaseHandler):
    def __init__(self, *args, **kwargs):
        super(MainHandler, self).__init__(*args, **kwargs)

    def index(self):
        # list posts
        query = {}
        tag = self.get_argument('tag', '').lower()
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
        featured_posts = list(Content.objects(featured=True, deleted=False, **query).order_by('-date_created'))

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
        self.render('main/index.html', **self.vars)

    @tornado.web.asynchronous
    def new(self):
        self.render('main/new.html', **self.vars)
