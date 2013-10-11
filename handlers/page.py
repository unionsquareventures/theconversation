import settings
import tornado.web
from base import BaseHandler
from models import Company, Post
from slugify import slugify

class PageHandler(BaseHandler):
	def __init__(self, *args, **kwargs):
		super(PageHandler, self).__init__(*args, **kwargs)
		
	def get(self):
		if self.request.path.find("/about") == 0:
			self.about()
		elif self.request.path.find("/portfolio") == 0:
			current = Company.objects(status="current").order_by('name')
			exited = Company.objects(status="exited").order_by('name')
			self.vars.update ({
				'current': current,
				'exited': exited,
				'slugify': slugify
			})
			self.render('page/portfolio.html', **self.vars)
		elif self.request.path.find("/network") == 0:
			self.network()
		elif self.request.path.find("/tools") == 0:
			self.render('page/tools.html', **self.vars)
		elif self.request.path.find("/jobs") == 0:
			self.render('page/jobs.html', **self.vars)
		else:
			super(PageHandler, self).get(id, action)
		
	def about(self):
		related_posts = Post.objects(tags__in=["thesis"], user__username__in=settings.staff_twitter_handles).order_by('-date_created')[:6]
		self.vars.update({
			'related_posts': related_posts
		})
		self.render('page/about.html', **self.vars)
		
	def network(self):
		related_posts = Post.objects(tags__in=["usv-network"], user__username__in=settings.staff_twitter_handles).order_by('-date_created')[:6]
		self.vars.update({
			'related_posts': related_posts
		})
		self.render('page/network.html', **self.vars)
		
	
					