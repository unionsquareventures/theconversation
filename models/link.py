import settings
from markdown import markdown

from mongoengine import *
from user import User
from content import Content
from custom_fields import ImprovedURLField
from urlparse import urlparse

class Link(Content):
    url = ImprovedURLField(max_length=65000, required=True, min_length=3)

    def validate(self, clean=True):
        errors = {}
        link = Link.objects(url=self._data['url'])
        if link:
            errors['url'] = ValidationError('This URL has already been submitted', field_name='url')

        try:
            super(Link, self).validate(clean=clean)
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

