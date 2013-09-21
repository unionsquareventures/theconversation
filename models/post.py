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
        'indexes': ['-date_deleted', 'deleted', '-date_featured',
                            'featured', 'voted_users', 'user.id_str', 'slug',
                            'slugs', 'url', 'tags'],
    }

    # Full text search index
    def __init__(self, *args, **kwargs):
        super(Post, self).__init__(*args, **kwargs)
        db = self._get_db()
        pcoll = db['post']

        pcoll.ensure_index([
            ('body_text', 'text'),
            ('title', 'text'),
            ('tags', 'text'),
            ('user.username', 'text'),
        ])


    date_created = DateTimeField(required=True)
    title = ImprovedStringField(required=True, max_length=1000, min_length=3)
    slugs = ListField(StringField())
    slug = StringField()
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

    def add_slug(self, title):
        slug = slugify(title)
        counter_coll = self._get_collection_name() + 'Slug'
        counter = self._get_db()[counter_coll].find_and_modify(query={'_id': slug},
                                                                update={'$inc': {'value': 1}},
                                                                upsert=True, new=True)
        if counter['value'] != 1:
            slug = '%s-%i' % (counter['_id'], counter['value'])
        self._data['slugs'] = self._data.get('slugs', []) + [slug]
        self._data['slug'] = slug
        return slug


    def set_fields(self, **kwargs):
        for fname in self._fields.keys():
            if kwargs.has_key(fname):
                setattr(self, fname, kwargs[fname])


    def save(self, *args, **kwargs):
        self.body_length_limit = kwargs.get('body_length_limit', None)
        self.validate()
        title_changed = hasattr(self, '_changed_fields') and 'title' in self._changed_fields
        if (title_changed or not self._data.get('slug')) and len(self._data.get('slugs', [])) < 6:
            try:
                self.add_slug(unicode(self._data['title']))
            except:
                self.add_slug(unicode(self._data['title'].decode('utf-8')))
            if hasattr(self, '_changed_fields'):
                self._changed_fields += ['slug', 'slugs']
        super(Post, self).save(*args, **kwargs)


    def validate(self, clean=True):
        errors = {}

        url = self._data.get('url', '')
        if url:
            post = Post.objects(url=self._data['url']).first()
            if post and (post.id != self._data['id'] or self._created):
                errors['url'] = ValidationError('This URL has already been submitted', field_name='url')

        hackpad = self._data.get('hackpad_url', '')
        if hackpad and self._data.get('has_hackpad'):
            base_domain = urlparse(hackpad).netloc
            valid_hackpad_domains = ['hackpad.com', 'www.hackpad.com', '%s.hackpad.com' % settings.hackpad['domain']]
            if base_domain not in valid_hackpad_domains:
                errors['hackpad_url'] = ValidationError('Invalid Hackpad URL', field_name='hackpad_url')

        #if self.body_length_limit:
        #    raw = self._data.get('body_raw', '')
        #    soup = BeautifulSoup(raw)
        #    if len(soup.get_text()) > self.body_length_limit:
        #        errors['body_raw'] = ValidationError('Post content exceeds %i characters'\
        #                                        % self.body_length_limit, field_name='body_raw')

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


