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
    hackpad_id = StringField(max_length=65000)
    has_hackpad = BooleanField()

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

            if field.__class__ == BooleanField:
                """
                field_html = '<input name="{name}" type="checkbox" class="post_{name}"' \
                                        ' value="true" id="post_{name}"/>'\
                                        '<label for="post_{name}">{placeholder}</label>'

                """
                field_html = '<button class="btn btn-large btn-block" type="button">{placeholder}</button>'

            if not field_html:
                continue

            value = self._data.get(name)
            value = value.replace('"', '\\"') if value else ''

            placeholder = placeholders.get(name, '')
            wrapper = lambda x: x
            if isinstance(placeholder, tuple):
                wrapper = placeholder[1]
                placeholder = placeholder[0]
            try:
                print wrapper('')
            except:
                import pdb
                pdb.set_trace()
            field_html = wrapper(field_html.format(name=name, value=value,
                                                                placeholder=placeholder))
            label = self.labels.get(name, name).title()
            field_errors = form_errors.get(name)

            yield (name, label, field_html, field_errors)
