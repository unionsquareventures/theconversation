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
    hackpad_url = StringField(max_length=65000)

    def form_fields(self, form_errors=None, form_fields=[]):
        for form_field in form_fields:
            field = self._fields[form_field['name']]
            # Ignore ID field and ignored fields
            if form_field['name'] == self._meta['id_field'] or form_field['name'] in self.ignored_fields:
                continue

            # Fill value
            value = self._data.get(form_field['name']) or ''
            if isinstance(value, str):
                value = value.replace('"', '\\"')
            form_field['value'] = value

            # Generate the correct HTML
            field_html = ''
            if form_field.get('hidden'):
                field_html = '<input name="{name}" type="hidden" class="link_{name}"' \
                                                            ' value="{value}" />'
            elif field.__class__ == StringField and not field.max_length:
                field_html = '<textarea name="{name}" class="link_{name}"' \
                                        'placeholder="{placeholder}">{value}</textarea>'
            elif field.__class__ == StringField and field.max_length:
                field_html = '<input name="{name}" type="text" class="link_{name}"' \
                                        ' placeholder="{placeholder}" value="{value}" />'
            elif field.__class__ == BooleanField:
                field_html = '<input name="{name}" type="checkbox" class="link_{name}"' \
                                        ' value="true" id="link_{name}" %s />'\
                                                        % ('checked' if form_field['value'] else '')
            field_html = field_html.format(**form_field)

            # Add label
            if form_field.has_key('label'):
                label = '<label for="link_{name}" data-selected="{label_selected}">{label}</label>'
                form_field['label_selected'] = form_field.get('label_selected', '').replace('"', "'")
                field_html += label.format(**form_field)

            if not field_html:
                continue

            # Wrap the element with the provided wrapping function
            wrapper = form_field.get('wrapper', lambda x: x)
            field_html = wrapper(field_html)

            # Handle errors and return
            field_errors = form_errors.get(form_field['name'])
            yield (form_field['name'], field_html, field_errors)
