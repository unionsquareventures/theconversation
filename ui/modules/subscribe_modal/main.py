import os
import tornado.web

class MainModule(tornado.web.UIModule):

	def render(self, **kwargs):
		full_uri = self.request.uri
		path = os.path.dirname(os.path.realpath(__file__))
		
		finished = False
		if 'finished' in self.request.arguments:
			finished = True
		
		if not finished:
			return self.render_string(os.path.join(path, 'main.html'),
								full_uri=full_uri, **kwargs)
		else:
			return