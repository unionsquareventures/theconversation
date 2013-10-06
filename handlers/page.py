import settings
import tornado.web
from base import BaseHandler


class PageHandler(BaseHandler):
	def __init__(self, *args, **kwargs):
		super(PageHandler, self).__init__(*args, **kwargs)
		
	def get(self):
		if self.request.path == "/portfolio/":
			self.render('page/portfolio.html', **self.vars)
		else:
			super(PageHandler, self).get(id, action)