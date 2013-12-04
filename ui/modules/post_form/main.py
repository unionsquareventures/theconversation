import os
import tornado.web
from models.post import Post
import mongoengine

def field_errors(errors, field):
    errors = errors.get(field)
    if not errors:
        return ''
    return errors.message

class MainModule(tornado.web.UIModule):
    name = ''
    wrap_javascript = False
    has_javascript = False

    def embedded_javascript(self):
        if self.has_javascript:
            return "%s();\n" % self.name

    def render(self, **kwargs):
        if not kwargs.get('post'):
            kwargs['post'] = Post()
        kwargs['errors'] = kwargs.get('errors', {})
        kwargs['existing_posts'] = kwargs.get('existing_posts', [])
        path = os.path.dirname(os.path.realpath(__file__))
        return self.render_string(os.path.join(path, 'main.html'),
                                field_errors=field_errors, **kwargs)

