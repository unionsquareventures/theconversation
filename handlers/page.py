import settings
import tornado.web
from base import BaseHandler
from models import Company, Post
from slugify import slugify

class PageHandler(BaseHandler):
	def __init__(self, *args, **kwargs):
		super(PageHandler, self).__init__(*args, **kwargs)
		
	def get(self):
		if self.request.path == "/about/":
			self.about()
		elif self.request.path == "/portfolio/":
			current = Company.objects(status="current").order_by('name')
			exited = Company.objects(status="exited").order_by('name')
			self.vars.update ({
				'current': current,
				'exited': exited,
				'slugify': slugify
			})
			self.render('page/portfolio.html', **self.vars)
		elif self.request.path == "/network/":
			self.network()
		else:
			super(PageHandler, self).get(id, action)
		
	def about(self):
		related_posts = Post.objects(tags__in=["about-page"]).order_by('-date_created')
		self.vars.update({
			'related_posts': related_posts
		})
		self.render('page/about.html', **self.vars)
		
	def network(self):
		related_posts = Post.objects(tags__in=["network-page"]).order_by('-date_created')
		self.vars.update({
			'related_posts': related_posts
		})
		self.render('page/network.html', **self.vars)
		
	
					