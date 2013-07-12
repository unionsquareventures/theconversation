import settings
import tornado.web
import tornado.auth
import tornado.httpserver
from base import BaseHandler
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
        per_page = 50
        sort_by = self.get_argument('sort_by', 'hot')
        page = abs(int(self.get_argument('page', '1')))
        posts = Content.objects(featured=False, deleted=False, **query).order_by(*ordering[sort_by])
        posts = posts[(page - 1) * per_page:(page - 1) * per_page + (per_page -1)]
        post_count = Content.objects(featured=False, deleted=False, **query).count()
        featured_posts = list(Content.objects(featured=True, deleted=False, **query).order_by('-date_featured'))

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
            'post_count': post_count,
            'page': page,
            'per_page': per_page,
            'featured_posts': featured_posts,
            'tags': tags,
            'current_tag': tag,
            'urlparse': urlparse,
        })
        self.render('main/index.html', **self.vars)

    @tornado.web.asynchronous
    def new(self):
        self.render('main/new.html', **self.vars)
