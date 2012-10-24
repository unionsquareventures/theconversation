import settings
from markdown import markdown
from lib.markdown.mdx_video import VideoExtension
import datetime as dt

from mongoengine import *
from question import Question
from annotation import Annotation
from user import User
from content import Content

class Post(Content):
    body_html = StringField(required=True)
    annotations = ListField(EmbeddedDocumentField(Annotation))

    labels = {
        'body_raw': 'body',
    }
    ignored_fields = ['body_html']
