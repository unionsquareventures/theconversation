import settings

from mongoengine import *
from user import User
from content import Content

class Post(Content):
    hackpad_id = StringField(max_length=65000, required=False)
    hackpad_url = StringField(max_length=65000, required=False)

    body_raw = StringField(required=True, min_length=10)
    body_html = StringField(required=True)

    ignored_fields = ['body_html']

