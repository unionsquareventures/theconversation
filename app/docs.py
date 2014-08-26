"""
Make it so we can view the auto-generated docs.<br />
Docs are built using [this fork of Pycco](https://github.com/nickgrossman/quezo-pycco/).
"""
import app.basic
import tornado.web
import settings


###########################
### View a docs page
### /docs /docs(?P<path>[A-z-+0-9+/.+//]+)
###########################
class ViewPage(app.basic.BaseHandler):
	@tornado.web.authenticated
	def get(self, path="index.html"):
		if not self.current_user_can('view_docs'):
			raise tornado.web.HTTPError(401)

		# path starts with docs/ 
		self.render(path)

	def get_template_path(self):
		"""
		Override default templates location.  Use template docs instead.
		"""
		return "docs"	