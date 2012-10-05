import settings
import tornado.web
import tornado.auth
import tornado.httpserver
from markdown import markdown
from lib.markdown.mdx_video import VideoExtension
import datetime as dt
import re
from collections import defaultdict

from base import BaseHandler
from minifier import Minifier

import mongoengine
from models import Post, User, Question

minifier = Minifier()

class EmailHandler(BaseHandler):
    def __init__(self, *args, **kwargs):
        super(EmailHandler, self).__init__(*args, **kwargs)
        self.vars['minifier'] = minifier

    def check_xsrf_cookie(self):
        pass

    def post(self):
        f = open("email", "w")
        f.write(self.request.body)
        f.close()
        self.write('OK')
        return
        """
        attributes = {k: v[0] for k, v in self.request.arguments.iteritems()}
        video_ext = VideoExtension(configs={})
        body_raw = attributes.get('body_raw', '')
        body_html = markdown(body_raw, extensions=[video_ext],
                                    output_format='html5', safe_mode=False)
        attributes.update({
            'user': User(**self.get_current_user()),
            'body_html': body_html,
        })
        attributes['tags'] = attributes.get('tags', '').split(' ')
        post = Post(**attributes)
        try:
            post.save()
        except mongoengine.ValidationError, e:
            print e
            self.new(model=post, errors=e.errors)
            return

        # Obtain questions
        questions_data = defaultdict(dict)
        for key, value in attributes.iteritems():
            if not key.startswith('question['):
                continue
            m = re.search(r"question\[([0-9]+)\]\[([A-z0-9\_]+)\]", key)
            index = int(m.group(1))
            field = m.group(2)
            questions_data[index][field] = value

        # Create questions
        for q in questions_data.values():
            # Ignore empty questions
            if not q["text"]:
                continue
            q = Question(**q)
            post.update(push__questions=q)

        self.redirect('/posts/%s' % minifier.int_to_base62(post.id))
        """
