from mongoengine import *
import re

# Add more readable error messages
class ImprovedStringField(StringField):
    def validate(self, value):
        if not isinstance(value, basestring):
            self.error('StringField only accepts string values')

        if self.max_length is not None and len(value) > self.max_length:
            self.error('Must be less than %i characters' % self.max_length)

        if self.min_length is not None and len(value) < self.min_length:
            self.error('Must be at least %i characters' % self.min_length)

        if self.regex is not None and self.regex.match(value) is None:
            self.error('Invalid input')


class ImprovedURLField(ImprovedStringField):
    _URL_REGEX = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    def __init__(self, url_regex=None, **kwargs):
        self.url_regex = url_regex or self._URL_REGEX
        super(ImprovedURLField, self).__init__(**kwargs)

    def validate(self, value):
        super(ImprovedURLField, self).validate(value)

        if value and not self.url_regex.match(value):
            self.error('Invalid URL')
            return

