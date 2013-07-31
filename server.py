import settings
import tornado.web
import tornado.auth
from tornado.httpserver import HTTPServer
import logging
from tornado.options import define, options
import sys
import os
import mimetypes
import json
import urlparse
import ssl
import functools
from raven.contrib.tornado import AsyncSentryClient

from handlers.base import BaseHandler
from handlers.post import PostHandler
from handlers.auth import TwitterLoginHandler, LogoutHandler
from handlers.fake_error import FakeErrorHandler
from handlers.deleted_posts import DeletedPostsHandler
from handlers.featured_posts import FeaturedPostsHandler
from handlers.hackpad import HackpadHandler
from handlers.delete_user import DeleteUserHandler
import ui
from redis import StrictRedis
from lib.sendgrid import Sendgrid

define("port", default=8888, help="run on the given port", type=int)

if __name__ == '__main__':
    tornado.options.parse_command_line()

    # Connect to Redis with a 50 msec timeout
    redis = StrictRedis(host=settings.redis_host,
                    port=settings.redis_port, db=0, socket_timeout=.05)

    # Sendgrid API
    sendgrid = Sendgrid(settings.sendgrid_user, settings.sendgrid_secret)

    # Bundle JS/CSS
    logging.info('Bundling JS/CSS')
    ui.template_processors.bundle_styles()
    ui.template_processors.bundle_javascript()

    logging.info('Starting server on port %s' % options.port)
    application = tornado.web.Application([
            (r'/auth/twitter/', TwitterLoginHandler),
            (r'/auth/logout/?', LogoutHandler),

            (r'/fake_error/?', FakeErrorHandler),
            (r'/delete_user/?', DeleteUserHandler),
            (r'/deleted_posts/?', DeletedPostsHandler),
            (r'/featured_posts/?', FeaturedPostsHandler),

            (r'/?', PostHandler),
            (r'/posts/?', PostHandler),
            (r'/posts/(?P<action>upvote)$', PostHandler),
            (r'/posts/(?P<action>new)$', PostHandler),
            (r'/posts/(?P<id>[\w\s-]+$)', PostHandler),
            (r'/posts/(?P<id>[\w\s-]+)/(?P<action>.*)$', PostHandler),
            (r'/generate_hackpad/?', HackpadHandler),
            ], ui_modules = ui.template_modules(),
            ui_methods = ui.template_methods(),
            redis=redis,
            sendgrid=sendgrid,
            **settings.tornado_config)

    # Initialize Sentry
    application.sentry_client = AsyncSentryClient(settings.sentry_dsn)

    application.listen(options.port)
    io_loop = tornado.ioloop.IOLoop.instance()

    # Watch the modules JS and CSS files for changes.
    # Re-bundle the JS/CSS accordingly upon modification.
    if settings.tornado_config['debug']:
        logging.info('Watching UI modules for changes...')
        ui.watch_modules(io_loop)

    io_loop.start()
