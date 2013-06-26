import settings

from mongoengine import *
from user import User
from content import Content
from custom_fields import ImprovedStringField, ImprovedURLField
from urlparse import urlparse

class Post(Content):
    hackpad_url = ImprovedURLField(max_length=65000, required=False)

    body_raw = ImprovedStringField(required=True, min_length=10)
    body_html = ImprovedStringField(required=True)

    ignored_fields = ['body_html']

    def validate(self, clean=True):
        errors = {}

        hackpad = self._data.get('hackpad_url', '')
        if hackpad:
            base_domain = urlparse(hackpad).netloc
            valid_hackpad_domains = ['hackpad.com', 'www.hackpad.com', '%s.hackpad.com' % settings.hackpad['domain']]
            if base_domain not in valid_hackpad_domains:
                errors['hackpad_url'] = ValidationError('Invalid Hackpad URL', field_name='hackpad_url')

        try:
            super(Post, self).validate(clean=True)
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
