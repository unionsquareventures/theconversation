import settings
import tornado.web
import tornado.auth
import tornado.httpserver

from base import BaseHandler

class PostHandler(BaseHandler):
    def get(self, id='', action=''):
        print "ID: %s" % id

        if id:
            # post detail page
            id = minifier.base62_to_int(id)
            res = self.db.posts.find_one({'_id': int(id)})
            if not res:
                raise tornado.web.HTTPError(404)
            self.render('templates/posts/get.html', **self.vars)
        else:
            # list posts
            self.render('templates/posts/index.html', **self.vars)

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
        # create a new post
        self.render('templates/posts/new.html', **self.vars)

    @tornado.web.authenticated
    def update(self):
        # update a post
        self.render('templates/posts/update.html', **self.vars)

