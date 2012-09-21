import settings
from markdown import markdown
from lib.markdown.mdx_video import VideoExtension
import datetime as dt

from mongoengine import *
from user import User

from minifier import Minifier

minifier = Minifier()

class IntIDMixin(object):
    def hook_id(self):
        counter_coll = self._get_collection_name() + 'Counter'
        counter = self._get_db()[counter_coll].find_and_modify(query={'_id': 'object_counter'},
                                                                update={'$inc': {'value': 1}},
                                                                upsert=True, new=True)
        id = counter['value']
        self._data['id'] = id

    def minified_id(self):
        return minifier.int_to_base62(self.id)

class BaseDocument(Document, IntIDMixin):
    labels = {}
    ignored_fields = []

    def save(self, *args, **kwargs):
        if kwargs.get('force_insert') or '_id' not in self.to_mongo():
            if self.hook_id:
                self.hook_id()
            if self.hook_date_created:
                self.hook_date_created()
        super(BaseDocument, self).save(*args, **kwargs)

    def form_fields(self, form_errors=None):
        for name, field in self._fields.iteritems():
            if name == self._meta['id_field'] or name in self.ignored_fields:
                continue

            if field.__class__ != StringField:
                continue
            field_html = '<textarea name="{name}">{value}</textarea>'
            if field.__class__ == StringField and field.max_length:
                field_html = '<input name="{name}" type="text" value="{value}" />'

            value = self._data.get(name)
            value = value.replace('"', '\\"') if value else ''
            field_html = field_html.format(name=name, value=value)
            label = self.labels.get(name, name).title()
            field_errors = form_errors.get(name)
            yield (name, label, field_html, field_errors)
