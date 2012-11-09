import settings
import datetime as dt
import re
from collections import defaultdict
from itertools import groupby
from operator import itemgetter
import os
import json
import urllib2
from pytz import timezone
import datetime as dt

import mongoengine
from models import Tweet, User, Tag

import c_t
sjson = c_t.ex

#search_req = urllib2.urlopen('http://search.twitter.com/search.json?q=%40usv').read()
#sjson = json.loads(search_req)

for tweet in sjson['results']:
    print tweet
    date_created = dt.datetime.strptime(tweet['created_at'], '%a, %d %b %Y %H:%M:%S +0000')
    date_created = date_created.replace(tzinfo=timezone('GMT'))
    date_created = date_created.astimezone(timezone('US/Eastern'))

    tweet = Tweet(
        user = User(auth_type='twitter', username=tweet['from_user']),
        title = '',
        body_raw = tweet['text'],
        body_html = '',
        tweet_id = tweet['id_str'],
        featured = False,
        date_created = date_created,
    )
    tweet.save()

