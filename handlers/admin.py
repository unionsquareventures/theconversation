import settings
from models.post import Post
from models.user_info import UserInfo
from base import BaseHandler
from urlparse import urlparse
import tornado
import datetime as dt
import urllib
import datetime
import time

class AdminHandler(BaseHandler):
	def get(self, action=None):
		if action == 'update_comment_counts':
			self.update_comment_counts()
		elif action == 'sort_posts':
			self.sort_posts()
		elif action == 'stats':
			self.stats()
		else:
			self.index()


	def index(self):
		self.render('admin/index.html', **self.vars)
		
	def stats(self):
		total_posts = Post.objects(date_created__gte="2013-08-01").count()
		total_users = UserInfo.objects().count()
		
		self.vars.update({
			'total_posts': total_posts,
			'total_users': total_users
		})
		self.render("admin/stats.html", **self.vars)
		
	def sort_posts(self):
		redis = self.settings['redis']
		data = []
		
		config = {
			'staff_bonus': int(self.get_argument('staff_bonus')) 
				if 'staff_bonus' in self.request.arguments else -3,
			'time_penalty_multiplier': float(self.get_argument('time_penalty_multiplier')) 
				if 'time_penalty_multiplier' in self.request.arguments else 3,
			'grace_period': float(self.get_argument('grace_period')) 
				if 'grace_period' in self.request.arguments else 0,
			'comments_multiplier': float(self.get_argument('comments_multiplier')) 
				if 'comments_multiplier' in self.request.arguments else 3,
			'votes_multiplier': float(self.get_argument('votes_multiplier')) 
				if 'votes_multiplier' in self.request.arguments else 1,
			'min_votes': float(self.get_argument('min_votes')) 
			if 'min_votes' in self.request.arguments else 2,
		}
		
		posts = Post.objects(deleted=False, votes__gte=config['min_votes']).order_by('-date_created')
		
		for i,post in enumerate(posts):
			tdelta = datetime.datetime.now() - post.date_created
			hours_elapsed = tdelta.seconds/3600 + tdelta.days*24
			
			base_score = post.downvotes * -1
			
			staff_bonus = 0
			if self.is_staff(post.user.username):
				staff_bonus = config['staff_bonus']
			
			time_penalty = 0
			if hours_elapsed > config['grace_period']:
				time_penalty = hours_elapsed - config['grace_period']
			if hours_elapsed > 22:
				time_penalty = time_penalty * 1.5
			
			votes_base_score = 0
			if post.votes == 1 and post.comment_count > 2:
				votes_base_score = -2
			if post.votes > 8 and post.comment_count == 0:
				votes_base_score = -2
			
			scores = {
				'votes': votes_base_score + post.votes * config['votes_multiplier'],
				'comments': post.comment_count * config['comments_multiplier'],
				'time': time_penalty * config['time_penalty_multiplier'] * -1
			}
			
			score = base_score + scores['votes'] + scores['comments'] + staff_bonus + scores['time']
			
			data.append({
				'username': post.user.username,
				'title': post.title,
				'id': post.id,
				'date_created': post.date_created,
				'hours_elapsed': hours_elapsed,
				'votes': post.votes,
				'comment_count': post.comment_count,
				'staff_bonus': staff_bonus,
				'time_penalty': time_penalty,
				'score': score,
				'scores': scores
			})
			data = sorted(data, key=lambda k: k['score'], reverse=True)
			
			if 'update' in self.request.arguments and self.get_argument('update') == "true":
				redis.zadd('hot_albacore', score , post.id)
		
		self.vars.update({
			'posts': posts,
			'data': data,
			'now': datetime.datetime.now(),
			'grace_period': config['grace_period'],
			'comments_multiplier': config['comments_multiplier'],
			'time_penalty_multiplier': config['time_penalty_multiplier'],
			'staff_bonus': config['staff_bonus'],
			'votes_multiplier': config['votes_multiplier'],
			'min_votes': config['min_votes']
		})
		self.render('admin/sort_posts.html', **self.vars)

	@tornado.web.asynchronous
	@tornado.web.authenticated
	def update_comment_counts(self):
		http = tornado.httpclient.AsyncHTTPClient()

		request_vars = {
			'api_key': settings.disqus_public_key,
			'api_secret': settings.disqus_secret_key,
			'forum': settings.disqus_apikey
		}

		base_url = "https://disqus.com/api/3.0/threads/list.json"
		complete_url = base_url + "?" + urllib.urlencode(request_vars)

		def on_disqus_response(response):
			#if response.error: raise tornado.web.HTTPError(500)
			result = tornado.escape.json_decode(response.body)
	
			for thread in result['response']:
				self.write(thread['id'] + " | " + thread['identifiers'][0] + " | " + thread['title'] + " | " + str(thread['posts']) + "<br />")
				post = Post.objects(id=thread['identifiers'][0]).first()
				try:
					post.update(set__comment_count=thread['posts'])
					#post.update(set__disqus_thread_id_str=thread['id'])
					#post.update(unset__disqus_thread_id_str=True)
					self.write("&uarr; updated<br />")    
				except: 
					self.write("&uarr; NOT updated<br />")  
					
			self.finish()
		
		http.fetch(tornado.httpclient.HTTPRequest(
			url=complete_url,
			method="GET"
			), 
			callback=on_disqus_response)

	@tornado.web.asynchronous
	@tornado.web.authenticated
	def update_disqus_urls(self):
		# EVENTUALLY, this can correct the URLs disqus stores about each thread
		# for our migration
		"""
		
		def on_disqus_response(self, response):
			#
			self.finish()
		
		http.fetch({
		'url': complete_url,
		'method': "POST"
		}, 
		callback=self.on_disqus_response)
		
		"""
		pass
