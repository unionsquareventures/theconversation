import settings
from models.post import Post
from models.user_info import UserInfo
from base import BaseHandler
from urlparse import urlparse
import tornado
import datetime as dt
import urllib

class AdminHandler(BaseHandler):
	def get(self, action=None):
		if action == 'update_comment_counts':
			self.update_comment_counts()
		else:
			self.index()

	def index(self):
		self.render('admin/index.html', **self.vars)

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
					post.update(unset__disqus_thread_id_str=True)
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
		http = tornado.httpclient.AsyncHTTPClient()
	
		request_vars = {
			'api_key': settings.disqus_public_key,
			'api_secret': settings.disqus_secret_key,
			'forum': settings.disqus_apikey
		}
	
		base_url = "https://disqus.com/api/3.0/threads/list.json"
		complete_url = base_url + "?" + urllib.urlencode(request_vars)
	
		def on_disqus_response(self, response):
			#if response.error: raise tornado.web.HTTPError(500)
			result = tornado.escape.json_decode(response.body)
		
			for thread in result['response']:
				#self.write(thread['identifiers'][0] + " | " + thread['title'] + " | " + str(thread['posts']) + "<br />")
				post = Post.objects(id=thread['identifiers'][0]).first()
				try:
					post.update(set__comment_count=thread['posts'])
					self.write("&uarr; updated<br />")    
				except: 
					raise tornado.web.HTTPError(500)

			self.finish()
		
		http.fetch({
		'url': complete_url,
		'method': "POST"
		}, 
		callback=self.on_disqus_response)
