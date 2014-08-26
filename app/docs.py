"""
Make it so we can view the auto-generated docs.<br />
Docs are built using [this fork of Pycco](https://github.com/nickgrossman/quezo-pycco/).

Here's how it works:

Documentation is automatically generated from [docstrings](https://www.python.org/dev/peps/pep-0257/) and inline comments.

Whenever you add comments or update docstrings, if you want the documentation to get updated, you need to run `pycco` by hand:

Install this custom version of pycco: [https://github.com/nickgrossman/quezo-pycco/](https://github.com/nickgrossman/quezo-pycco/) -- download the code as a zip file, unzip it, then, from the command line, cd into the unzipped directory and run:

`$ setup.py install`

Next, cd into your application's code directory (for example: `$ cd ~/dev/theconversation`), and run pycco:

`$ pycco . -p`

The "." tells pycco to run in the current directory, and "-p" tells it to use the default file location (the `docs/` folder)

This will overwrite your existing docs, which is fine -- since they are both just auto-generated from the codebase.  Commit them:

`$ git add docs`

`$ git commit -m "docs updated!"`

etc.
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
	def get(self, path=None):
		if not self.current_user_can('view_docs'):
			raise tornado.web.HTTPError(401)
		
		if not path:
			self.redirect('/docs/index.html')
			
		# path starts with docs/ 
		self.render(path)

	def get_template_path(self):
		"""
		Override default templates location.  Use template docs instead.
		"""
		return "docs"	