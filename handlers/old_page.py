from base import BaseHandler
import tornado
import settings
from urlparse import urlparse

class OldPageHandler(BaseHandler):
	def get(self, filepath=''):
		
		if self.request.path.find('/team/brad.html') == 0:
			new_url = 'http://' + self.request.host + '/about#brad-burnham'
		
		elif self.request.path.find('/team/fred.html') == 0:
			new_url = 'http://' + self.request.host + '/about#fred-wilson'
		
		elif self.request.path.find('/team/albert.html') == 0:
			new_url = 'http://' + self.request.host + '/about#albert-wenger'
			
		elif self.request.path.find('/team') == 0:
			new_url = 'http://' + self.request.host + '/about'
		
		elif self.request.path.find('/focus') == 0:
			new_url = 'http://' + self.request.host + '/about'
		
		elif self.request.path.find('/investments') == 0:
			new_url = 'http://' + self.request.host + '/portfolio'
		
		elif self.request.path.find('/pages') == 0:
				
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
