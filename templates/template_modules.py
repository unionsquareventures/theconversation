import os
import sys
from tornado.web import UIModule
import logging

sys.path.append('../')
import settings

"""
		Iterate through the modules folder, creating UIModules for each module.

		- JavaScript for each module is externally bundled and loaded into the page.
		- The embedded_javascript method of BaseUIModule is called when a module is
		used in a template. It provides additional JavaScript for the page to
		contain. Modules with JavaScript will invoke their externally bundled
		JavaScript by injecting a call to it into the parent template.
"""

class BaseUIModule(UIModule):
		name = ''
		wrap_javascript = False

		def __init__(self, *args, **kwargs):
				super(BaseUIModule, self).__init__(*args, **kwargs)

		def embedded_javascript(self):
				if self.has_javascript:
						return "%s();\n" % self.name

		def render(self, *args, **kwargs):
				relpath = "{name}/main.html".format(name=self.name)
				filepath = os.path.join(settings.get('module_dir'), relpath)
				return self.render_string(filepath, *args, **kwargs)

# Create modules using the folder name as the module name
def template_modules():
		modules = {}
		for filename in os.listdir(settings.get('module_dir')):
				path = os.path.join(settings.get('module_dir'), filename)
				if not os.path.isdir(path):
						continue

				# Open JS file, check for contents
				js_file = os.path.join(path, "main.js")
				has_javascript = False
				try:
						f = open(js_file, 'r')
						if f.read().strip():
								has_javascript = True
						f.close()
				except IOError:
						pass

				# Create a UIModule object for this module
				modules[filename] = type("UI_%s" % filename, (BaseUIModule,), {
						'name': filename,
						'has_javascript': has_javascript
				})
		return modules

