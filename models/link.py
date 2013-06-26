import settings
from markdown import markdown

from mongoengine import *
from user import User
from content import Content
from custom_fields import ImprovedURLField

class Link(Content):
    url = ImprovedURLField(max_length=65000, required=True, min_length=3, unique=True)

