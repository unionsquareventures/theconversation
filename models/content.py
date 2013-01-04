import settings
from markdown import markdown
from lib.markdown.mdx_video import VideoExtension
import datetime as dt

from mongoengine import *
from question import Question
from user import User
from annotation import Annotation

class Content(Document):
    body_raw = StringField(required=True)
    body_html = StringField(required=True)
    id = IntField(primary_key=True)
    title = StringField(required=True, max_length=1000)
    date_created = DateTimeField(required=True)
    user = EmbeddedDocumentField(User, required=True)
    questions = ListField(EmbeddedDocumentField(Question))
    tags = ListField(StringField())
    featured = BooleanField(default=False)
    votes = IntField(default=0)
    voted_users = ListField(EmbeddedDocumentField(User))
    annotations = ListField(EmbeddedDocumentField(Annotation))

    meta = {'allow_inheritance': True}
    ignored_fields = ['body_html']

    def hook_date_created(self):
        if not self._data.get('date_created'):
            self._data['date_created'] = dt.datetime.now()

    def hook_id(self):
        counter_coll = self._get_collection_name() + 'Counter'
        counter = self._get_db()[counter_coll].find_and_modify(query={'_id': 'object_counter'},
                                                                update={'$inc': {'value': 1}},
                                                                upsert=True, new=True)
        id = counter['value']
        self._data['id'] = id

    def save(self, *args, **kwargs):
        if kwargs.get('force_insert') or '_id' not in self.to_mongo():
            if self.hook_id:
                self.hook_id()
            if self.hook_date_created:
                self.hook_date_created()
        super(Content, self).save(*args, **kwargs)

    def form_fields(self, form_errors=None):
        for name, field in self._fields.iteritems():
            if name == self._meta['id_field'] or name in self.ignored_fields:
                continue

            field_html = ''
            if field.__class__ == StringField and not field.max_length:
                field_html = '<textarea name="{name}">{value}</textarea>'
            if field.__class__ == StringField and field.max_length:
                field_html = '<input name="{name}" type="text" value="{value}" />'

            if not field_html:
                continue

            value = self._data.get(name)
            value = value.replace('"', '\\"') if value else ''
            field_html = field_html.format(name=name, value=value)
            label = self.labels.get(name, name).title()
            field_errors = form_errors.get(name)

            yield (name, label, field_html, field_errors)
