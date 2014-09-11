import pymongo
import re
import settings
import json
from datetime import datetime
from datetime import date
from datetime import timedelta
from urlparse import urlparse
from slugify import slugify
from mongoengine import *
from lib import sanitize
from decimal import *

from lib.custom_fields import ImprovedStringField, ImprovedURLField
from lib.userdb import User

#
# Embedded Comment
#
class Comment(EmbeddedDocument):
    def __init__(self, *args, **kwargs):
        super(Comment, self).__init__(*args, **kwargs)
        db = self._get_db()

    author_email = StringField()
    user = EmbeddedDocumentField(User, required=True)
    date_created = DateTimeField(required=True)
    body_raw = ImprovedStringField(required=False, default="")
    body_text = ImprovedStringField(required=False, default="")
    body_html = ImprovedStringField(required=False, default="")
    status = StringField(default="published")

    def set_fields(self, **kwargs):
        for fname in self._fields.keys():
            if kwargs.has_key(fname):
                setattr(self, fname, kwargs[fname])