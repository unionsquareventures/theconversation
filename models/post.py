import settings
from markdown import markdown
from lib.markdown.mdx_video import VideoExtension
import datetime as dt

from mongoengine import *
from user import User

from minifier import Minifier

minifier = Minifier()

class Post(Document):
    id = IntField(primary_key=True)
    title = StringField(required=True, max_length=1000)
    body_raw = StringField(required=True)
    body_html = StringField(required=True)
    date_created = DateTimeField(required=True)
    user = EmbeddedDocumentField(User, required=True)

    labels = {
        'body_raw': 'body',
    }
    ignored_fields = ['body_html']

    def minified_id(self):
        return minifier.int_to_base62(self.id)

    def hook_id(self):
        counter = self._get_db().postsCounter.find_and_modify(query={'_id': 'object_counter'},
                                                      update={'$inc': {'value': 1}},
                                                      upsert=True, new=True)
        id = counter['value']
        self._data['id'] = id

    def hook_date_created(self):
        self._data['date_created'] = dt.datetime.now()

    def save(self, *args, **kwargs):
        if kwargs.get('force_insert') or '_id' not in self.to_mongo():
            self.hook_id()
            self.hook_date_created()

        super(Post, self).save(*args, **kwargs)

    def form_fields(self):
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
            print name
            field_html = field_html.format(name=name, value=value)
            label = self.labels.get(name, name)
            yield (label, field_html)
