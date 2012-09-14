import settings
import tornado.web
import tornado.auth
import tornado.httpserver

from base import BaseHandler
from minifier import Minifier

minifier = Minifier()

class PostHandler(BaseHandler):
    def get(self, params=''):
        if params.find('/') == -1:
            params += '/'
        id, action = params.split('/')
        # Route new, detail, and index
        if id == 'new':
            self.new()
            return
        if id and action == '':
            self.detail(id)
            return
        if action == 'edit':
            self.edit()
            return
        self.index()

    def index(self):
        # list posts
        self.render('templates/posts/index.html', **self.vars)

    def detail(self, id):
        id = minifier.base62_to_int(id)
        res = self.db.posts.find_one({'_id': int(id)})
        if not res:
            raise tornado.web.HTTPError(404)
        self.render('templates/posts/get.html', **self.vars)

    @tornado.web.authenticated
    def post(self):
        # create the post
        pass

    @tornado.web.authenticated
    def put(self, id=''):
        # update a post
        pass

    @tornado.web.authenticated
    def new(self):
        # form to create a new post
        self.render('templates/posts/new.html', **self.vars)

    @tornado.web.authenticated
    def edit(self):
        # form to update a post
        self.render('templates/posts/update.html', **self.vars)

