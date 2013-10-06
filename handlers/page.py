import settings
import tornado.web
from base import BaseHandler


class PageHandler(BaseHandler):
	def __init__(self, *args, **kwargs):
		super(PageHandler, self).__init__(*args, **kwargs)
		
	def get(self):
		if self.request.path == "/about/":
			self.render('page/about.html', **self.vars)
		elif self.request.path == "/portfolio/":
			self.render('page/portfolio.html', **self.vars)
		elif self.request.path == "/network/":
			self.render('page/network.html', **self.vars)
		else:
			super(PageHandler, self).get(id, action)