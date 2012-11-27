import settings
import tornado.web
import tornado.auth
from tornado.httpserver import HTTPServer
import sys
import os
import mimetypes
import json
import urlparse
import ssl

from handlers.base import BaseHandler
from handlers.post import PostHandler
from handlers.link import LinkHandler
from handlers.tweet import TweetHandler
from handlers.disqus import DisqusHandler
from handlers.annotation import AnnotationHandler
from handlers.auth import TwitterLoginHandler
from handlers.email import EmailHandler
import ui

log = settings.log

# Main page
class IndexHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        self.redirect('/posts')

if __name__ == '__main__':
    log.info('Bundling CSS/JS')
    ui.template_processors.bundle_styles()
    ui.template_processors.bundle_javascript()
    log.info('Starting server')
    application = tornado.web.Application([
        (r'/', IndexHandler),
        (r'/auth/twitter/', TwitterLoginHandler),
        # Posts
        (r'/posts$', PostHandler),
        (r'/posts/(?P<action>upvote)$', PostHandler),
        (r'/posts/(?P<action>new)$', PostHandler),
        (r'/posts/(?P<id>[A-z0-9]+$)', PostHandler),
        (r'/posts/(?P<id>[A-z0-9]+)/(?P<action>.*)$', PostHandler),
        # Links
        (r'/links$', LinkHandler),
        (r'/links/(?P<action>upvote)$', LinkHandler),
        (r'/links/(?P<action>new)$', LinkHandler),
        (r'/links/(?P<id>[A-z0-9]+$)', LinkHandler),
        (r'/links/(?P<id>[A-z0-9]+)/(?P<action>.*)$', LinkHandler),
        # Tweets
        (r'/tweets/(?P<action>upvote)$', TweetHandler),
        (r'/tweets/(?P<id>[A-z0-9]+$)', TweetHandler),
        (r'/tweets/(?P<id>[A-z0-9]+)/(?P<action>.*)$', TweetHandler),
        # Disqus
        (r'/disqus', DisqusHandler),
        # Annotations
        (r'/annotations', AnnotationHandler),
        (r'/annotations/(?P<id>\d+$)', AnnotationHandler),
        # Email
        (r'/email$', EmailHandler),
    ], ui_modules = ui.template_modules,
        ui_methods = ui.template_methods,
         **settings.tornado_config)

    if settings.server_port == 443:
        log.info('SSL enabled')
        server = HTTPServer(application, ssl_options=dict(
            certfile="keys/server.crt",
            keyfile="keys/server.key",
            cert_reqs=ssl.CERT_NONE,
        ))
        server.listen(settings.server_port)
    else:
        log.info('SSL disabled')
        application.listen(settings.server_port)

    tornado.ioloop.IOLoop.instance().start()
