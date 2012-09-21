import settings
from markdown import markdown
from lib.markdown.mdx_video import VideoExtension
import datetime as dt

from mongoengine import *
from base import BaseDocument
from user import User

class Post(BaseDocument):
    title = StringField(required=True, max_length=1000)
    body_raw = StringField(required=True)
    body_html = StringField(required=True)
    date_created = DateTimeField(required=True)
    user = EmbeddedDocumentField(User, required=True)

    labels = {
        'body_raw': 'body',
    }
    ignored_fields = ['body_html']

    def hook_date_created(self):
        self._data['date_created'] = dt.datetime.now()
