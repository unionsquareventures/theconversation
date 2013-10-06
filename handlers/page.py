import settings
import tornado.web
from base import BaseHandler
from models import Company
from slugify import slugify

class PageHandler(BaseHandler):
	def __init__(self, *args, **kwargs):
		super(PageHandler, self).__init__(*args, **kwargs)
		
	def get(self):
		if self.request.path == "/about/":
			self.render('page/about.html', **self.vars)
		elif self.request.path == "/portfolio/":
			current = Company.objects(status="current").order_by('name')
			exited = Company.objects(status="exited").order_by('name')
			cos = Company.objects()
			for co in cos:
				url = co.title.replace(" ", "").lower() + ".com"
				self.write(url)
			return
			self.vars.update ({
				'current': current,
				'exited': exited,
				'slugify': slugify
			})
			self.render('page/portfolio.html', **self.vars)
		elif self.request.path == "/network/":
			self.render('page/network.html', **self.vars)
		else:
			super(PageHandler, self).get(id, action)

		
					