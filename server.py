import settings
import tornado.web
import tornado.auth
from tornado.httpserver import HTTPServer
from tornado.options import define, options, logging
import sys
import os
import mimetypes
import json
import urlparse
import ssl
import functools

from handlers.base import BaseHandler
from handlers.link import LinkHandler
from handlers.auth import TwitterLoginHandler
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
            # Links
            (r'/', LinkHandler),
            (r'/links$', LinkHandler),
            (r'/links/(?P<action>upvote)$', LinkHandler),
            (r'/links/(?P<action>new)$', LinkHandler),
            (r'/links/(?P<id>[A-z0-9]+$)', LinkHandler),
            (r'/links/(?P<id>[A-z0-9]+)/(?P<action>.*)$', LinkHandler),
        ], ui_modules = ui.template_modules(),
            ui_methods = ui.template_methods(),
            **settings.tornado_config)

    application.listen(options.port)
    io_loop = tornado.ioloop.IOLoop.instance()

    # Watch the modules JS and CSS files for changes.
    # Re-bundle the JS/CSS accordingly upon modification.
    if settings.tornado_config['debug']:
        logging.info('Watching UI modules for changes...')
        ui.watch_modules(io_loop)

    io_loop.start()
