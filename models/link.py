import settings
from markdown import markdown
from lib.markdown.mdx_video import VideoExtension
import datetime as dt

from mongoengine import *
from question import Question
from annotation import Annotation
from user import User
from content import Content

class Link(Content):
    url = StringField(required=True, max_length=65000)

    labels = {
    }
    ignored_fields = []
