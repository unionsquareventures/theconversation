import settings
from markdown import markdown
from lib.markdown.mdx_video import VideoExtension
import datetime as dt

from mongoengine import *
from question import Question
from annotation import Annotation
from user import User
from content import Content

class Link(Content):
    url = StringField(max_length=65000)
    content = StringField(max_length=65000)
    content_type = StringField(max_length=250)

    def form_fields(self, form_errors=None, placeholders={}, order=[]):
        if order:
            ffields = [(fname, self._fields.get(fname)) for fname in order]
        else:
            ffields = self._fields.iteritems()

        for name, field in ffields:
            if name == self._meta['id_field'] or name in self.ignored_fields:
                continue

            field_html = ''
            if field.__class__ == StringField and not field.max_length:
                field_html = '<textarea name="{name}" class="post_{name}"' \
                                            ' placeholder="{placeholder}">{value}</textarea>'
            if field.__class__ == StringField and field.max_length:
                field_html = '<input name="{name}" type="text" class="post_{name}"' \
                                                ' placeholder="{placeholder}" value="{value}" />'

            if not field_html:
                continue

            value = self._data.get(name)
            value = value.replace('"', '\\"') if value else ''
            field_html = field_html.format(name=name, value=value,
                                           placeholder=placeholders.get(name, ''))
            label = self.labels.get(name, name).title()
            field_errors = form_errors.get(name)

            yield (name, label, field_html, field_errors)
