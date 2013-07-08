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
from handlers.link import LinkHandler
from handlers.main import MainHandler
from handlers.auth import TwitterLoginHandler, LogoutHandler
from handlers.fake_error import FakeErrorHandler
from handlers.deleted_content import DeletedContentHandler
from handlers.hackpad import HackpadHandler
import ui

define("port", default=8888, help="run on the given port", type=int)

if __name__ == '__main__':
    tornado.options.parse_command_line()

    # Bundle JS/CSS
    logging.info('Bundling JS/CSS')
    ui.template_processors.bundle_styles()
    ui.template_processors.bundle_javascript()

    logging.info('Starting server on port %s' % options.port)
    application = tornado.web.Application([
            (r'/auth/twitter/', TwitterLoginHandler),
            (r'/auth/logout/?', LogoutHandler),

            (r'/fake_error/?', FakeErrorHandler),
            (r'/deleted_content/?', DeletedContentHandler),

            (r'/', MainHandler),
            (r'/(?P<action>new)$', MainHandler),

            (r'/links/?', LinkHandler),
            (r'/links/(?P<action>upvote)$', LinkHandler),
            (r'/links/(?P<action>new)$', LinkHandler),
            (r'/links/(?P<id>[A-z0-9]+$)', LinkHandler),
            (r'/links/(?P<id>[A-z0-9]+)/(?P<action>.*)$', LinkHandler),

            (r'/posts/?', PostHandler),
            (r'/posts/(?P<action>upvote)$', PostHandler),
            (r'/posts/(?P<action>new)$', PostHandler),
            (r'/posts/(?P<id>[A-z0-9]+$)', PostHandler),
            (r'/posts/(?P<id>[A-z0-9]+)/(?P<action>.*)$', PostHandler),
            (r'/get_hackpad/?', HackpadHandler),
            ], ui_modules = ui.template_modules(),
            ui_methods = ui.template_methods(),
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
