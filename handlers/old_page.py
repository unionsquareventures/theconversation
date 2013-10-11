from base import BaseHandler
import tornado
import settings
from urlparse import urlparse

class OldPageHandler(BaseHandler):
	def get(self, filepath=''):
		
		# Old Team Pages
		team = [
			'brad-burnham',
			'fred-wilson',
			'albert-wenger',
			'john-buttrick',
			'andy-weissman',
			'nick-grossman',
			'kerri-rachlin',
			'veronica-keaveney',
			'gillian-campbell',
			'brittany-laughlin',
			'alexander-pease',
			'brian-watson'
		]
		for person in team:
			if self.request.path.find('/pages/' + person) == 0:
				new_url = 'http://' + self.request.host + '/about#' + person
		
		if not new_url:
			raise tornado.web.HTTPError(404)
		else:
			self.redirect(new_url, permanent=True)
