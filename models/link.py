import settings
from markdown import markdown

from mongoengine import *
from user import User
from content import Content

class Link(Content):
    url = StringField(max_length=65000, required=True)

