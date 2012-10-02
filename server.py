import settings
import tornado.web
import tornado.auth
import tornado.httpserver
import sys
import os
import mimetypes
import json
import urlparse
import forms

from handlers.base import BaseHandler
from handlers.post import PostHandler
from handlers.disqus import DisqusHandler
from handlers.annotation import AnnotationHandler
from handlers.auth import TwitterLoginHandler

log = settings.log

# Main page
class IndexHandler(BaseHandler):
    def get(self):
        self.redirect('/posts')

if __name__ == '__main__':
    log.info('Starting server on port 8888')
    application = tornado.web.Application([
        (r'/', IndexHandler),
        (r'/auth/twitter/', TwitterLoginHandler),
        # Posts
        (r'/posts$', PostHandler),
        (r'/posts/(?P<action>new)$', PostHandler),
        (r'/posts/(?P<id>[A-z0-9]+$)', PostHandler),
        (r'/posts/(?P<id>[A-z0-9]+)/(?P<action>.*)$', PostHandler),
        # Disqus
        (r'/disqus', DisqusHandler),
        # Annotations
        (r'/annotations', AnnotationHandler),
        (r'/annotations/(?P<id>\d+$)', AnnotationHandler),
    ], **settings.tornado_config)
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
