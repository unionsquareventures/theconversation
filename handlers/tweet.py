import settings
import tornado.web
import tornado.auth
import tornado.httpserver
import datetime as dt
import re
from collections import defaultdict
from itertools import groupby
from operator import itemgetter
import os
import pytz
from base import BaseHandler

import mongoengine
from models import Tweet, User

class TweetHandler(BaseHandler):
    def __init__(self, *args, **kwargs):
        super(TweetHandler, self).__init__(*args, **kwargs)

    def detail(self, id):
        tweet = Tweet.objects(id=id).first()
        if not tweet:
            raise tornado.web.HTTPError(404)
        self.vars.update({
            'tweet': tweet,
            'pytz': pytz,
        })
        self.render('tweets/get.html', **self.vars)

    @tornado.web.authenticated
    def get(self, id='', action=''):
        if action == 'upvote' and id:
            self.upvote(id)
        else:
            super(TweetHandler, self).get(id, action)

    def upvote(self, id):
        username = self.get_current_user()['username']
        user_q = {'$elemMatch': {'username': username}}
        tweet = Tweet.objects(id=id).fields(voted_users=user_q).first()
        if not tweet:
            raise tornado.web.HTTPError(404)
        detail = self.get_argument('detail', '')
        if tweet.voted_users:
            self.redirect(('/tweets/%s?error' % tweet.id) if detail else '/posts?error')
            return


        tweet.update(inc__votes=1)
        tweet.update(push__voted_users=User(**self.get_current_user()))

        self.redirect(('/tweets/%s' % tweet.id) if detail else '/posts')
