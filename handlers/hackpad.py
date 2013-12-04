import tornado.web
from handlers.base import BaseHandler
from lib.hackpad import HackpadAPI
import settings

class HackpadHandler(BaseHandler):
    @tornado.web.authenticated
    @tornado.web.asynchronous
    def get(self):
        hackpad_api = HackpadAPI(settings.hackpad['oauth_client_id'],
                                            settings.hackpad['oauth_secret'],
                                            domain=settings.hackpad['domain'])
        def hpad_created(hpad_json):
            hackpad_url = 'https://%s.hackpad.com/%s'\
                                            % (settings.hackpad['domain'], hpad_json['padId'])
            self.write(hackpad_url)
            self.finish()
        hackpad_api.create(hpad_created)
