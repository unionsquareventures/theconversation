import settings
from markdown import markdown
import datetime as dt

from mongoengine import *
from user import User
from custom_fields import ImprovedStringField

class Content(Document):
    meta = {
        'allow_inheritance': True,
        'indexes': ['votes', 'date_created', 'tags'],
    }

    id = IntField(primary_key=True)
    date_created = DateTimeField(required=True)
    title = ImprovedStringField(required=True, max_length=1000, min_length=5)
    user = EmbeddedDocumentField(User, required=True)
    tags = ListField(ImprovedStringField())
    votes = IntField(default=0)
    voted_users = ListField(EmbeddedDocumentField(User))
    deleted = BooleanField(default=False)
    featured = BooleanField(default=False)
    date_featured = DateTimeField(required=False)

    ignored_fields = []

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
        if kwargs.get('force_insert') or '_id' not in self.to_mongo() or self._created:
            if self.hook_date_created:
                self.hook_date_created()
            self._data['id'] = 0
            self.validate()
            if self.hook_id:
                  self.hook_id()
        super(Content, self).save(*args, **kwargs)

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
            elif isinstance(field, StringField) and not field.max_length:
                field_html = '<textarea name="{name}" class="link_{name}"' \
                                        'placeholder="{placeholder}">{value}</textarea>'
            elif isinstance(field, StringField) and field.max_length:
                field_html = '<input name="{name}" type="text" class="link_{name}"' \
                                        ' placeholder="{placeholder}" value="{value}" />'
            elif isinstance(field, BooleanField):
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
