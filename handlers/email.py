import settings
import tornado.web
import tornado.auth
import tornado.httpserver
from markdown import markdown
from lib.markdown.mdx_video import VideoExtension
import datetime as dt
import re
from collections import defaultdict
import json

from base import BaseHandler

import mongoengine
from models import Post, User, Question

class EmailHandler(BaseHandler):
    def __init__(self, *args, **kwargs):
        super(EmailHandler, self).__init__(*args, **kwargs)

    def check_xsrf_cookie(self):
        pass

    def post(self):
        f = open("email", "w")
        f.write(self.request.body)
        f.close()
        email = json.loads(self.request.body)
        #video_ext = VideoExtension(configs={})
        #body_html = markdown(body_raw, extensions=[video_ext],
        #                            output_format='html5', safe_mode=False)
        user_info = {
                    'auth_type': 'email',
                    'username': email['headers']['Sender']
        }
        attributes = {
            'user': User(**user_info),
            'title': email['headers']['Subject'],
            'body_html': email['html'],
            'body_raw': email['html'],
        }
        post = Post(**attributes)
        try:
            post.save()
        except mongoengine.ValidationError, e:
            raise tornado.web.HTTPError(400)
            return
        self.write('OK')
