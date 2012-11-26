import os
import sys
from tornado.web import UIModule
import settings

"""
Iterate through the _modules folder, creating UIModules for each module.
If javascript for the module exists, ensure it's wrapper method is called.
"""

modules = {}
moduledir = os.path.join(settings.tornado_config['template_path'], '_modules')

class BaseUIModule(tornado.web.UIModule):
    name = ''
    wrap_javascript = False

    def __init__(self, *args, **kwargs):
        super(BaseUIModule, self).__init__(*args, **kwargs)

    def embedded_javascript(self):
        if self.wrap_javascript:
            return "%s();\n" % self.name

    def render(self, *args, **kwargs):
        relpath = "{name}/main.html".format(name=self.name)
        filepath = os.path.join(moduledir, relpath)
        return self.render_string(filepath, *args, **kwargs)

for file in os.listdir(moduledir):
    path = os.path.join(moduledir, folder)
    if not os.path.isdir(path):
        continue
    # Create a module using the folder name
    js_file = os.path.join(path, "main.js")
    # todo: open JS file, check for contents, set wrap_javascript

    modules[name] = type("UI_%s" % name, (BaseUIModule,), {
        'name': name,
        'wrap_javascript': 
    })
