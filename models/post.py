import settings
from markdown import markdown
from user_info import User, VotedUser
from urlparse import urlparse
from bs4 import BeautifulSoup
from slugify import slugify
from mongoengine import *
from custom_fields import ImprovedStringField, ImprovedURLField
mongodb_db = urlparse(settings.mongodb_url).path[1:]
connect(mongodb_db, host=settings.mongodb_url)

class Post(Document):
    meta = {
        'indexes': ['date_deleted', 'deleted', 'date_featured',
                            'featured', 'voted_users', 'user.id_str'],
    }

    # Full text search index
    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args, **kwargs)
        db = self._get_db()
        pcoll = db['post']
        pcoll.ensure_index([
            ('body_text', 'text'),
            ('title', 'text'),
            ('user.username', 'text'),
        ])


    id = StringField(primary_key=True)
    date_created = DateTimeField(required=True)
    title = ImprovedStringField(required=True, max_length=1000, min_length=3)
    user = EmbeddedDocumentField(User, required=True)
    tags = ListField(ImprovedStringField())
    votes = IntField(default=0)
    voted_users = ListField(EmbeddedDocumentField(VotedUser))
    deleted = BooleanField(default=False)
    date_deleted = DateTimeField(required=False)
    featured = BooleanField(default=False)
    date_featured = DateTimeField(required=False)
    url = ImprovedURLField(max_length=65000, required=False)
    hackpad_url = ImprovedURLField(max_length=65000)
    has_hackpad = BooleanField(default=False)
    body_raw = ImprovedStringField(required=True, min_length=10)
    body_html = ImprovedStringField(required=True)
    body_truncated = ImprovedStringField(required=True)
    body_text = ImprovedStringField(required=True)


    def hook_id(self):
        slug = slugify(unicode(self._data['title']))
        counter_coll = self._get_collection_name() + 'Slug'
        counter = self._get_db()[counter_coll].find_and_modify(query={'_id': slug},
                                                                update={'$inc': {'value': 1}},
                                                                upsert=True, new=True)
        if counter['value'] != 1:
            slug = '%s-%i' % (counter['_id'], counter['value'])
        self._data['id'] = slug


    def set_fields(self, **kwargs):
        for fname in self._fields.keys():
            if kwargs.has_key(fname):
                setattr(self, fname, kwargs[fname])


    def save(self, *args, **kwargs):
        self.body_length_limit = kwargs.get('body_length_limit', None)
        if kwargs.get('force_insert') or '_id' not in self.to_mongo() or self._created:
            self._data['id'] = ''
            self.validate()
            if self.hook_id:
                  self.hook_id()
        super(Post, self).save(*args, **kwargs)


    def validate(self, clean=True):
        errors = {}

        url = self._data.get('url', '')
        if url:
            post = Post.objects(url=self._data['url']).first()
            if post and (post.id != self._data['id'] or self._created):
                errors['url'] = ValidationError('This URL has already been submitted', field_name='url')

        hackpad = self._data.get('hackpad_url', '')
        if hackpad:
            base_domain = urlparse(hackpad).netloc
            valid_hackpad_domains = ['hackpad.com', 'www.hackpad.com', '%s.hackpad.com' % settings.hackpad['domain']]
            if base_domain not in valid_hackpad_domains:
                errors['hackpad_url'] = ValidationError('Invalid Hackpad URL', field_name='hackpad_url')

        if self.body_length_limit:
            raw = self._data.get('body_raw', '')
            soup = BeautifulSoup(raw)
            if len(soup.get_text()) > self.body_length_limit:
                errors['body_raw'] = ValidationError('Post content exceeds %i characters'\
                                                % self.body_length_limit, field_name='body_raw')

        try:
            super(Post, self).validate(clean=clean)
        except ValidationError, e:
            errors.update(e.errors)

        if errors:
            pk = 'None'
            if hasattr(self, 'pk'):
                pk = self.pk
            elif self._instance:
                pk = self._instance.pk
            message = 'ValidationError (%s:%s) ' % (self._class_name, pk)
            raise ValidationError(message, errors=errors)


    def form_fields(self, form_errors=None, form_fields=[]):
        for form_field in form_fields:
            field = self._fields[form_field['name']]

            # Fill value
            value = self._data.get(form_field['name']) or ''
            if isinstance(value, str):
                value = value.replace('"', '\\"')
            form_field['value'] = value

            # Generate the correct HTML
            field_html = ''
            if form_field.get('hidden'):
                field_html = '<input name="{name}" type="hidden" class="post_{name}"' \
                                                            ' value="{value}" />'
            elif isinstance(field, StringField) and not field.max_length:
                field_html = '<textarea name="{name}" class="post_{name}"' \
                                        'placeholder="{placeholder}">{value}</textarea>'
            elif isinstance(field, StringField) and field.max_length:
                field_html = '<input name="{name}" type="text" class="post_{name}"' \
                                        ' placeholder="{placeholder}" value="{value}" />'
            elif isinstance(field, BooleanField):
                field_html = '<input name="{name}" type="checkbox" class="post_{name}"' \
                                        ' value="true" id="post_{name}" %s />'\
                                                        % ('checked' if form_field['value'] else '')
            field_html = field_html.format(**form_field)

            # Add label
            if form_field.has_key('label'):
                label = '<label for="post_{name}" data-selected="{label_selected}">{label}</label>'
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
