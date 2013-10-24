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
from handlers.auth import TwitterLoginHandler, LogoutHandler, CloseHandler
from handlers.fake_error import FakeErrorHandler
from handlers.deleted_posts import DeletedPostsHandler
from handlers.featured_posts import FeaturedPostsHandler
from handlers.hackpad import HackpadHandler
from handlers.delete_user import DeleteUserHandler
from handlers.blacklist_user import BlacklistUserHandler
from handlers.search import SearchHandler
from handlers.old_post import OldPostHandler
from handlers.email import EmailHandler
from handlers.page import PageHandler
from handlers.old_page import OldPageHandler
from handlers.api import APIHandler
from handlers.admin import AdminHandler
#from handlers.redirect import RedirectHandler
import ui
from redis import StrictRedis
from lib.sendgrid import Sendgrid
from lib.disqus import Disqus
import json

import newrelic.agent
path = os.path.join(settings.PROJECT_ROOT, 'server_setup/conf/newrelic.ini')
newrelic.agent.initialize(path, settings.DEPLOYMENT_STAGE)

define("port", default=8888, help="run on the given port", type=int)

class RedirectHandler(tornado.web.RequestHandler):
    def get(self, person=None):
        if person:
            self.redirect('http://www.usv.com/about#' + person, permanent=True)
        else:
            self.redirect('http://www.usv.com', permanent=True)

def init_app(bundle=True, auth_passthrough=False):
    sentry_client = AsyncSentryClient(settings.sentry_dsn)
    sendgrid = Sendgrid(settings.sendgrid_user, settings.sendgrid_secret, sentry_client)
    disqus = Disqus(settings.disqus_public_key, settings.disqus_secret_key,
                    settings.disqus_apikey, sentry_client)
    # Connect to Redis with a 200 msec timeout
    redis = StrictRedis.from_url(settings.redis_url, socket_timeout=.2)
    # Bundle JS/CSS
    if settings.tornado_config['debug'] and bundle:
        logging.info('Bundling JS/CSS')
        #ui.template_processors.bundle_styles()
        #ui.template_processors.bundle_javascript()
    # Old post URLs mapping
    f = open('old_post_urls.json', 'r')
    old_post_urls = json.loads(f.read())
    f.close()
    logging.info('Starting server on port %s' % options.port)
    application = tornado.web.Application([
            (r'/auth/twitter/', TwitterLoginHandler),
            (r'/auth/logout/?', LogoutHandler),
            (r'/auth/email/?', EmailHandler),
            (r'/auth/close_popup/?', CloseHandler),

            (r'/fake_error/?', FakeErrorHandler),
            (r'/delete_user/?', DeleteUserHandler),
            (r'/deleted_posts/?', DeletedPostsHandler),
            (r'/users/(?P<username>[A-z-+0-9]+)/(?P<action>.*)$', BlacklistUserHandler),
            (r'/featured.*$', FeaturedPostsHandler),
            (r'/search/?', SearchHandler),

            (r'/(?P<year>[0-9]+)/(?P<month>[0-9]+)/(?P<slug>[\w\s-]+).php$', OldPostHandler),
           
            (r'/pages/.*$', OldPageHandler),
            (r'/team.*$', OldPageHandler),
            (r'/investments$', OldPageHandler),
            (r'/focus$', OldPageHandler),

            (r'/portfolio.*$', PageHandler),
            (r'/portfolio/migrate$', PageHandler),
            (r'/about.*$', PageHandler),
            (r'/network.*$', PageHandler),
            (r'/tools.*$', PageHandler),
            (r'/jobs.*$', PageHandler),

            (r'/?', PostHandler),
            (r'/posts/?', PostHandler),
            (r'/(?P<action>tagged)/(?P<tag>[A-z-+0-9 ]*)$', PostHandler),
            (r'/posts/(?P<action>upvote)$', PostHandler),
            (r'/posts/(?P<action>new)$', PostHandler),
            (r'/posts/(?P<id>[\w\s-]+$)', PostHandler),
            (r'/posts/(?P<id>[\w\s-]+)/(?P<action>.*)$', PostHandler),
            (r'/feed/(?P<feed_type>[A-z-+0-9]+)$', PostHandler),
            (r'/feed$', PostHandler),
            
            (r'/generate_hackpad/?', HackpadHandler),

            # API calls
            (r'/api/user_status/?', APIHandler),
            
            (r'/admin/(?P<action>.*)$', AdminHandler),
            (r'/admin$', AdminHandler),

            # For redirects from old content.usv.com
            (r'/pages/(?P<person>[A-z-+0-9]+)$', RedirectHandler),
            (r'/pages/(?P<person>[A-z-+0-9]+)/$', RedirectHandler),
            (r'/.*$', RedirectHandler),
            
            ], ui_modules = ui.template_modules(),
            ui_methods = ui.template_methods(),
            redis=redis,
            sendgrid=sendgrid,
            disqus=disqus,
            old_post_urls=old_post_urls,
            auth_passthrough=auth_passthrough,
            **settings.tornado_config)
    application.sentry_client = sentry_client
    return application


if __name__ == '__main__':
    tornado.options.parse_command_line()
    application = init_app()
    application.listen(options.port)
    io_loop = tornado.ioloop.IOLoop.instance()

    # Watch the modules JS and CSS files for changes.
    # Re-bundle the JS/CSS accordingly upon modification.
    if settings.tornado_config['debug']:
        logging.info('Watching UI modules for changes...')
        ui.watch_modules(io_loop)

    io_loop.start()
