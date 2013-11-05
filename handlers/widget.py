import settings
import tornado.web
import tornado.auth
import tornado.escape
import tornado.httpserver
from tornado.httpclient import *
import os
import lib.sanitize as sanitize
from base import BaseHandler
import mongoengine
from models import Post
import json
from urlparse import urlparse
from datetime import datetime
import datetime as dt
import time
import re
import urllib

class WidgetHandler(BaseHandler):
	def __init__(self, *args, **kwargs):
		super(WidgetHandler, self).__init__(*args, **kwargs)

	def get(self):
		if self.request.path == '/widget':
			self.display_widget()
		if self.request.path == '/widget/demo':
			self.render('widget/demo.html', **self.vars)
	
	def display_widget(self):
		# list posts
		query = {}
		tag = self.get_argument('tag', '').lower()
		if tag:
			query.update({
				'tags': tag,
			})
		
		per_page = 4
		
		sort_by = "hot_albacore"
			
		anchor = self.get_argument('anchor', None)
		action = self.get_argument('action', '')
		count = int(self.get_argument('count', 0))
		if count < 0:
			count = 0
		
		original_count = count
		if action == 'before':
			count += per_page
		
		page = 1
		
		lua = "local num_posts = redis.call('ZCARD', '{sort_by}')\n"
		if anchor != None:
			anchor = Post.objects(id=anchor).first()
			if not anchor:
				raise tornado.web.HTTPError(400)
			if anchor.featured:
				lua += "local rank = {count}\n"
			else:
				lua += "local rank = redis.call('ZREVRANK', '{sort_by}', '{anchor.id}')\n"
				lua += "local rank = rank >= {count} - 1 and rank or {count}\n"
		
			if action == 'after':
				lua += "local rstart = rank + 1\n"
				lua += "local rend = rank + {per_page}\n"
			else:
				lua += "local rstart = rank - {per_page} >= 0 and rank - {per_page} or 0\n"
				lua += "local rend = rank - 1 >= 0 and rank - 1 or 0\n"
		else:
			lua += "local rank = 0\n"
			lua += "local rstart = 0\n"
			lua += "local rend = {per_page} - 1\n"
		redis = self.settings['redis']
		lua += "local ordered_ids = redis.call('ZREVRANGE', '{sort_by}', rstart, rend)\n"\
			   "return {{num_posts, rstart, rend, ordered_ids}}"
		lua = lua.format(per_page=per_page, sort_by=sort_by, anchor=anchor, count=count)
		get_posts = redis.register_script(lua)
		num_posts, rstart, rend, ordered_ids = get_posts()
		posts = Post.objects(id__in=ordered_ids)
		posts = {str(p.id): p for p in posts}
		posts = [posts[id] for id in ordered_ids]
		
		self.vars.update({
			'posts': posts
		})
		
		self.render('widget/widget.js', **self.vars)